from typing import Optional

from .custom_types import CourseData
from .diff import Diff, DiffCode


class Course:
    def __init__(self, data: Optional[CourseData]):
        self._data: Optional[CourseData] = data

    def get_data(self) -> Optional[CourseData]:
        return self._data

    def update_data(self, data: Optional[CourseData]) -> list[Diff]:
        if not data:
            return []

        if not self._data:
            self._data = data
            return [
                Diff(DiffCode.FIRST_FETCH, data["code"])
            ]

        diffs: list[Diff] = []

        course_code = self._data['code']
        old_sections = self._data['sections']
        new_sections = data['sections']

        compare_sections = [
            (old_sections.get(code), new_sections.get(code))
            for code in new_sections.keys() | old_sections.keys()
        ]

        for old_section, new_section in compare_sections:
            match old_section, new_section:
                case None, None:
                    pass

                case None, _:
                    diffs.append(Diff(
                        DiffCode.NEW_SECTION,
                        course_code,
                        new_section["code"],
                        new_section["free_seats"]
                    ))

                case _, None:
                    diffs.append(Diff(
                        DiffCode.SECTION_REMOVED,
                        course_code,
                        old_section["code"]
                    ))

                case _, _:
                    section_code = new_section['code']

                    match old_section['free_seats'], new_section['free_seats']:
                        case 0, free_seats if free_seats > 0:
                            diffs.append(Diff(
                                DiffCode.SEATS_BECAME_AVAILABLE,
                                section_code,
                                free_seats
                            ))

                        case taken_seats, 0 if taken_seats > 0:
                            diffs.append(Diff(
                                DiffCode.SEATS_BECAME_UNAVAILABLE,
                                section_code
                            ))

                        case seats_before, seats_after if seats_before > seats_after:
                            seats_before_thres = ((seats_before - 1) // 5) * 5
                            seats_after_thres = ((seats_after - 1) // 5) * 5

                            if seats_before_thres != seats_after_thres:
                                diffs.append(Diff(
                                    DiffCode.SEATS_DROPPED,
                                    section_code,
                                    seats_after
                                ))

                        case seats_before, seats_after if seats_before < seats_after:
                            seats_before_thres = (seats_before // 5) * 5
                            seats_after_thres = (seats_after // 5) * 5

                            if seats_before_thres != seats_after_thres:
                                diffs.append(Diff(
                                    DiffCode.SEATS_ROSE,
                                    section_code,
                                    seats_after
                                ))

                        case _:
                            pass

                    if old_section['professor'] != new_section['professor']:
                        diffs.append(Diff(
                            DiffCode.PROFESSOR_CHANGED,
                            section_code,
                            old_section["professor"],
                            new_section["professor"]
                        ))

        self._data = data
        return diffs
