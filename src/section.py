from typing import Any
from custom_types import SeatAvailability, SectionData


class Section:
    '''Represents a section with its details and methods to interact with section data. Feel free to add data as needed.'''

    def __init__(self, data: dict[str, Any]):
        section_data = data['Section']

        self.id = section_data['Id']
        self.name = section_data['SectionNameDisplay']
        self.course_id = section_data['CourseId']
        self.availability = SeatAvailability(
            availableSeats=int(section_data['Available']),
            totalSeats=int(section_data['Capacity']) if not (
                section_data['HasUnlimitedSeats']) else 999_999_999,
            waitlistSeats=int(section_data['Waitlisted'])
        )

        self.instructor = data['FacultyDisplay']

    def to_dict(self) -> SectionData:
        return {
            "sectionId": self.id,
            "name": self.name,
            "courseId": self.course_id,
            "instructor": self.instructor,
            "availability": {
                "availableSeats": self.availability["availableSeats"],
                "totalSeats": self.availability["totalSeats"],
                "waitlistSeats": self.availability["waitlistSeats"]
            }
        }

    @classmethod
    def from_dict(cls, data: SectionData) -> "Section":
        # Reconstructs the original "Section" structure expected by __init__
        return cls({
            "Section": {
                "Id": data["sectionId"],
                "SectionNameDisplay": data["name"],
                "CourseId": data["courseId"],
                "Available": str(data["availability"]["availableSeats"]),
                "Capacity": str(data["availability"]["totalSeats"]),
                "Waitlisted": str(data["availability"]["waitlistSeats"]),
                "HasUnlimitedSeats": data["availability"]["totalSeats"] == float("inf")
            },
            "FacultyDisplay": data["instructor"]
        })

    def __repr__(self):
        return f"<Section {self.id} - {self.name}>"

    def get_subject_code(self) -> str:
        return self.name.split("-")[0]

    def get_subject_number(self) -> int:
        return int(self.name.split("-")[1])
