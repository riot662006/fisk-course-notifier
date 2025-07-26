from typing import TypedDict

class SectionData(TypedDict):
    code: str
    professor: str
    free_seats: int

class CourseData(TypedDict):
    id: str
    code: str
    sections: dict[str, SectionData]
    fetch_timestamp: int

