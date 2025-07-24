import json
from typing import Any
from urllib.parse import urljoin

import requests

from .base_scraper import BASE_URL
from .section import Section
from .custom_types import CourseData, SectionsSearchCriteria


class Course:
    '''Represents a course with its details and methods to interact with course data. Feel free to add data as needed.'''

    def __init__(self, data: dict[str, Any]):
        self.id = data["Id"]
        self.section_ids = data["MatchingSectionIds"]
        self.title = data["Title"]
        self.subject_number = data["Number"]
        self.subject_code = data["SubjectCode"]

    def __repr__(self):
        return f"<Course {self.id} - {self.title}>"

    def to_dict(self) -> CourseData:
        return {
            "courseId": self.id,
            "sectionIds": self.section_ids,
            "title": self.title,
            "subjectNumber": self.subject_number,
            "subjectCode": self.subject_code
        }

    @classmethod
    def from_dict(cls, data: CourseData) -> 'Course':
        return cls({
            "Id": data["courseId"],
            "MatchingSectionIds": data["sectionIds"],
            "Title": data["title"],
            "Number": data["subjectNumber"],
            "SubjectCode": data.get("subjectCode")
        })

    def get_course_search_criteria(self) -> dict[str, Any]:
        return {
            "subjectCode": self.subject_code,
            "courseNumber": self.subject_number,
        }

    def get_sections_search_criteria(self) -> SectionsSearchCriteria:
        return {
            "courseId": self.id,
            "sectionIds": self.section_ids
        }

    def get_course_label(self) -> str:
        return self.subject_code + "-" + self.subject_number

    def fetch_sections(self, session: requests.Session) -> list[Section]:
        response = session.post(
            urljoin(BASE_URL, "Sections"),
            headers={
                'content-type': 'application/json, charset=UTF-8',
            },
            data=json.dumps(self.get_sections_search_criteria())
        )

        response.raise_for_status()

        term_and_sections = response.json(
        )["SectionsRetrieved"]["TermsAndSections"]

        return [
            Section(section_data)

            for term_and_section in term_and_sections
            for section_data in term_and_section['Sections']
        ]
