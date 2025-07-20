from custom_types import SeatAvailability, SectionData


class Section:
    '''Represents a section with its details and methods to interact with section data. Feel free to add data as needed.'''

    def __init__(self, data: dict[str, any]):
        section_data = data['Section']

        self.id = section_data['Id']
        self.name = section_data['SectionNameDisplay']
        self.course_id = section_data['CourseId']
        self.availability = SeatAvailability(
            availableSeats=int(section_data['Available']),
            totalSeats=int(section_data['Capacity']) if not (
                section_data['HasUnlimitedSeats']) else float('inf'),
            waitlistSeats=int(section_data['Waitlisted'])
        )

        self.instructor = data['FacultyDisplay']

    def to_dict(self) -> SectionData:
        return {
            "id": self.id,
            "name": self.name,
            "courseId": self.course_id,
            "instructor": self.instructor,
            "availability": {
                "available": self.availability["availableSeats"],
                "total": self.availability["totalSeats"],
                "waitlist": self.availability["waitlistSeats"]
            }
        }

    @classmethod
    def from_dict(cls, data: SectionData) -> "Section":
        # Reconstructs the original "Section" structure expected by __init__
        return cls({
            "Section": {
                "Id": data["id"],
                "SectionNameDisplay": data["name"],
                "CourseId": data["courseId"],
                "Available": str(data["availability"]["available"]),
                "Capacity": str(data["availability"]["total"]),
                "Waitlisted": str(data["availability"]["waitlist"]),
                "HasUnlimitedSeats": data["availability"]["total"] == float("inf")
            },
            "FacultyDisplay": data["instructor"]
        })

    def __repr__(self):
        return f"<Section {self.id} - {self.name}>"
