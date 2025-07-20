from typing import TypedDict


class SectionsSearchCriteria(TypedDict):
    courseId: int
    sectionIds: list[str]


class SeatAvailability(TypedDict):
    availableSeats: int
    totalSeats: int
    waitlistSeats: int


class CourseData(SectionsSearchCriteria):
    title: str
    subjectCode: str
    subjectNumber: str


class SectionData(TypedDict):
    sectionId: str
    name: str
    courseId: str
    instructor: str
    availability: SeatAvailability
