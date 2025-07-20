from custom_types import SeatAvailability


class Section:
    '''Represents a section with its details and methods to interact with section data. Feel free to add data as needed.'''

    def __init__(self, data: dict[str, any]):
        section_data = data['Section']

        self.id = section_data['Id']
        self.name = section_data['SectionNameDisplay']
        self.course_id = section_data['CourseId']
        self.availability = SeatAvailability(
            availableSeats=section_data['Available'],
            totalSeats=section_data['Capacity'] if not (
                section_data['HasUnlimitedSeats']) else float('inf'),
            waitlistSeats=section_data['Waitlisted']
        )

        self.instructor = data['FacultyDisplay']

    def __repr__(self):
        return f"<Section {self.id} - {self.name}>"
