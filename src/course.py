from custom_types import CourseData, SectionsSearchCriteria


class Course:
    '''Represents a course with its details and methods to interact with course data. Feel free to add data as needed.'''

    def __init__(self, data):
        self.id = data["Id"]
        self.section_ids = data["MatchingSectionIds"]
        self.title = data["Title"]
        self.subject_code = data["SubjectCode"]

    def __repr__(self):
        return f"<Course {self.id} - {self.title}>"

    def to_dict(self):
        return {
            "courseId": self.id,
            "sectionIds": self.section_ids,
            "title": self.title,
            "subjectCode": self.subject_code
        }

    def get_sections_search_criteria(self) -> SectionsSearchCriteria:
        return {
            "courseId": self.id,
            "sectionIds": self.section_ids
        }
