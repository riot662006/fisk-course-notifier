import time
from typing import Any

import requests
import json
from urllib.parse import urljoin

from .base_scraper import BASE_URL
from .course import Course
from .custom_types import CourseData
from .section import Section

COURSE_DATA_FILE_PATH = "output/course_data.json"
DEFAULT_POLL_INTERVAL = 60  # seconds


def fetch_courses(session: requests.Session, search_criteria: dict[str, Any]):
    response = session.post(
        urljoin(BASE_URL, "PostSearchCriteria"),
        headers={
            'content-type': 'application/json, charset=UTF-8',
        },
        data=json.dumps(search_criteria)
    )
    response.raise_for_status()

    courses = response.json()["Courses"]

    return [
        Course(
            course
        )
        for course in courses
    ]


def fetch_sections_by_course_labels(session: requests.Session, course_labels: list[str]) -> list[Section]:
    courses = fetch_courses(session, search_criteria={
        "keywordComponents": [{
            "subject": course_label.split("-")[0],
            "courseNumber": course_label.split("-")[1],
            "section": "",
            "synonym": ""
        } for course_label in course_labels]
    })

    return [
        section
        for course in courses
        for section in course.fetch_sections(session)
    ]


def load_courses(path: str = COURSE_DATA_FILE_PATH) -> dict[str, CourseData]:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError):
        raise ValueError(
            f"Could not load courses from {path}. File may be missing or corrupted."
        )


def save_courses(courses: list[Course], path: str = COURSE_DATA_FILE_PATH):
    with open(path, 'w') as f:
        json.dump({course.get_course_label(): course.to_dict()
                  for course in courses}, f, indent=4)


def watch_courses(
    labels: list[str],
    *,
    courses_save_path: str = COURSE_DATA_FILE_PATH,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
):
    session = requests.Session()

    # Build search criteria from course labels like "CSCI-101"
    search_criteria = {
        "keywordComponents": [
            {
                "subject": label.split("-")[0],
                "courseNumber": label.split("-")[1],
                "section": "",
                "synonym": ""
            }
            for label in labels
        ]
    }

    print("📡 Initial fetch...")
    previous_courses = fetch_courses(session, search_criteria)
    save_courses(previous_courses, courses_save_path)

    print(
        f"✅ Monitoring {len(previous_courses)} courses. Checking every {poll_interval} seconds.")

    while True:
        time.sleep(poll_interval)
        try:
            current_courses = fetch_courses(session, search_criteria)

            if current_courses != previous_courses:
                print("🔔 Change detected! Updating saved data.")
                save_courses(current_courses, courses_save_path)
                # Optionally: send_notification(current_courses)
                previous_courses = current_courses
            else:
                print("⏳ No changes detected.")
        except Exception as e:
            print(f"⚠️ Error during fetch: {e}")
