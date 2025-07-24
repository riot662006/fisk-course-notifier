from typing import Any

import requests
import json
from urllib.parse import urljoin

from .base_scraper import BASE_URL
from .course import Course
from .custom_types import CourseData
from .section import Section

COURSE_DATA_FILE_PATH = "output/course_data.json"


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
