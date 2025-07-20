from typing import Any
import pytest

from src.section import Section
from src.custom_types import SeatAvailability


@pytest.mark.parametrize("section_data, expected_availabilty", [
    (
        {
            "Id": 101,
            "SectionNameDisplay": "CSCI-101",
            "CourseId": 1,
            "Available": "30",
            "Capacity": "50",
            "Waitlisted": "0",
            "HasUnlimitedSeats": False
        },
        {
            "availableSeats": 30,
            "totalSeats": 50,
            "waitlistSeats": 0
        }
    ),
    (
        {
            "Id": 102,
            "SectionNameDisplay": "MATH-201",
            "CourseId": 2,
            "Available": "0",
            "Capacity": "0",
            "Waitlisted": "0",
            "HasUnlimitedSeats": True
        },
        {
            "availableSeats": 0,
            "totalSeats": None,  # Represents unlimited seats
            "waitlistSeats": 0
        }
    )
])
def test_section_init(section_data: dict[str, Any], expected_availabilty: SeatAvailability):
    section = Section({"Section": section_data, "FacultyDisplay": "Dr. Smith"})

    assert section.id == section_data["Id"]
    assert section.name == section_data["SectionNameDisplay"]
    assert section.course_id == section_data["CourseId"]
    assert section.instructor == "Dr. Smith"
    assert section.availability == expected_availabilty
