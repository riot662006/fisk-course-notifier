from typing import Any

import requests
import json
from urllib.parse import urljoin

from .base_scraper import BASE_URL
from .section import Section

from .course import Course


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
