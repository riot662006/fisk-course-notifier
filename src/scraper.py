from typing import Iterable

import json
import requests
import time
from urllib.parse import urljoin

from .base_scraper import BASE_URL
from .course import Course
from .custom_types import CourseData

COURSE_DATA_FILE_PATH = "output/course_data.json"
DEFAULT_POLL_INTERVAL = 60  # seconds


def fetch_courses(session: requests.Session, course_codes: list[str]) -> dict[str, Course]:
    response = session.post(
        urljoin(BASE_URL, "PostSearchCriteria"),
        headers={
            'content-type': 'application/json, charset=UTF-8',
        },
        data=json.dumps({
            "keywordComponents": [{
                "subject": course_code.split("-")[0],
                "courseNumber": course_code.split("-")[1],
            } for course_code in course_codes]
        })
    )
    response.raise_for_status()

    courses = [Course(course) for course in response.json()["Courses"]]

    return {
        course.get_course_label(): course
        for course in courses
    }


def load_courses(path: str = COURSE_DATA_FILE_PATH) -> dict[str, CourseData]:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError):
        raise ValueError(
            f"Could not load courses from {path}. File may be missing or corrupted."
        )


def save_courses(courses: Iterable[Course], path: str = COURSE_DATA_FILE_PATH):
    with open(path, 'w') as f:
        json.dump({course.get_course_label(): course.to_dict()
                  for course in courses}, f, indent=4)


def watch_courses(
    course_codes: list[str],
    *,
    courses_save_path: str = COURSE_DATA_FILE_PATH,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
):
    session = requests.Session()

    print("📡 Initial fetch...")
    previous_courses = fetch_courses(session, course_codes)
    save_courses(previous_courses.values(), courses_save_path)

    print(
        f"✅ Monitoring {len(previous_courses)} courses. Checking every {poll_interval} seconds.")

    while True:
        time.sleep(poll_interval)
        try:
            current_courses = fetch_courses(session, course_codes)

            if current_courses != previous_courses:
                print("🔔 Change detected! Updating saved data.")
                save_courses(current_courses.values(), courses_save_path)
                # Optionally: send_notification(current_courses)
                previous_courses = current_courses
            else:
                print("⏳ No changes detected.")
        except Exception as e:
            print(f"⚠️ Error during fetch: {e}")
