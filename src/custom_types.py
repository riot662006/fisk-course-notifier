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
    subjectCode: str | None


class SectionData(TypedDict):
    sectionId: str
    courseId: int
    instructor: str
    availability: SeatAvailability
