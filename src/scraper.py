from typing import Any

import requests
import json
from urllib.parse import urljoin

from .course import Course
from .custom_types import SectionsSearchCriteria
from .section import Section

BASE_URL = "https://fisk-ss.colleague.elluciancloud.com/Student/Courses/"


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


def fetch_sections(session: requests.Session, search_criteria: SectionsSearchCriteria):
    response = session.post(
        urljoin(BASE_URL, "Sections"),
        headers={
            'content-type': 'application/json, charset=UTF-8',
        },
        data=json.dumps(search_criteria)
    )
    response.raise_for_status()

    term_and_sections = response.json(
    )["SectionsRetrieved"]["TermsAndSections"]

    return [
        Section(section_data)

        for term_and_section in term_and_sections
        for section_data in term_and_section['Sections']
    ]

def fetch_sections_by_course_labels(session: requests.Session, course_labels: list[str]):
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
        for section in fetch_sections(session, course.get_sections_search_criteria())
    ]

