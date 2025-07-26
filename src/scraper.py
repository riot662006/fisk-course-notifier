from typing import Any

import json
import requests
import time
from urllib.parse import urljoin


from .base_scraper import BASE_URL
from .course import Course
from .custom_types import CourseData
from .diff import Diff

COURSE_DATA_FILE_PATH = "output/course_data.json"
DEFAULT_POLL_INTERVAL = 60  # seconds


def fetch(session: requests.Session, path: str, data: dict[str, Any]) -> dict[str, Any]:
    response = session.post(
        urljoin(BASE_URL, path),
        headers={
            'content-type': 'application/json, charset=UTF-8',
        },
        data=json.dumps(data)
    )

    response.raise_for_status()
    return response.json()


def fetch_course_data(session: requests.Session, _course_codes: list[str]) -> dict[str, CourseData]:
    course_codes = set(_course_codes)

    search_criteria = {
        "keywordComponents": [{
            "subject": course_code.split("-")[0],
            "courseNumber": course_code.split("-")[1],
        } for course_code in course_codes]
    }

    courses = fetch(session, "PostSearchCriteria", search_criteria)["Courses"]
    course_data: dict[str, CourseData] = {}

    for course in courses:
        course_code: str = course['SubjectCode'] + "-" + course['Number']

        if course_code in course_codes:
            course_id = course["Id"]
            section_ids: list[str] = course["MatchingSectionIds"]

            course_data[course_code] = {
                "id": course_id,
                "code": course_code,
                "sections": {},
                "fetch_timestamp": int(time.time())
            }

            terms_and_sections = fetch(session, "Sections", {
                "courseId": course_id, "sectionIds": section_ids})["SectionsRetrieved"]["TermsAndSections"]
            sections = [
                section
                for term_and_sections in terms_and_sections
                for section in term_and_sections["Sections"]
            ]

            for section in sections:
                section_id: str = section["Section"]["Id"]
                section_code: str = section["Section"]["SectionNameDisplay"]
                section_professor = section["FacultyDisplay"]
                free_seats = section["Section"]["Available"]

                course_data[course_code]["sections"][section_id] = {
                    "code": section_code,
                    "professor": section_professor,
                    "free_seats": free_seats
                }

    missing = course_codes - set(course_data.keys())
    if missing:
        raise ValueError(
            f"Missing course data for: {', '.join(sorted(missing))}")

    return course_data


def load_courses(path: str) -> dict[str, Course]:
    try:
        with open(path, 'r') as f:
            all_data: dict[str, CourseData] = json.load(f)
            return {code: Course(data) for code, data in all_data.items()}
    except (json.JSONDecodeError):
        raise ValueError(
            f"Could not load courses from {path}. File may be missing or corrupted."
        )


def update_courses(data: dict[str, Course], changes: dict[str, CourseData]) -> list[Diff]:
    return [
        diff
        for course_code in changes.keys()
        for diff in data.get(course_code, Course(None)).update_data(changes[course_code])
    ]


def save_courses(courses: dict[str, Course], path: str):
    with open(path, 'w') as f:
        course_data = {code: course.get_data()
                       for code, course in courses.items()}
        json.dump(course_data, f, indent=4)


def watch_courses(
    course_codes: list[str],
    *,
    courses_save_path: str = COURSE_DATA_FILE_PATH,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
):
    session = requests.Session()

    print("📡 Initial fetch...")
    course_data = fetch_course_data(session, course_codes)

    course_store = {code: Course(data) for code, data in course_data.items()}
    save_courses(course_store, courses_save_path)

    print(
        f"✅ Monitoring {len(course_store)} courses. Checking every {poll_interval} seconds.")

    while True:
        time.sleep(poll_interval)
        try:
            course_store = load_courses(courses_save_path)

            updates = fetch_course_data(session, course_codes)
            diffs = update_courses(course_store, updates)

            if diffs:
                visible_diffs = [d for d in diffs if not d.is_silent()]

                if visible_diffs:
                    print("🔔 Changes detected!")
                    for diff in visible_diffs:
                        print(diff)
                else:
                    print("⏳ No significant changes detected — silent diffs only.")

                print("💾 Updating store")
                save_courses(course_store, courses_save_path)

            else:
                print("⏳ No changes detected.")

        except Exception as e:
            print(f"⚠️ Error during fetch: {e}")
