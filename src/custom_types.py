from typing import TypedDict


class SectionsSearchCriteria(TypedDict):
    courseId: int
    sectionIds: list[str]


class CourseData(SectionsSearchCriteria):
    title: str
    subjectCode: str | None
