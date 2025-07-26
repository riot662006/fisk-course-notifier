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
            return []

        diffs: list[Diff] = []

        new_sections = data['sections'].keys() - self._data['sections'].keys()
        if len(new_sections):
            diffs.append(Diff(DiffCode.NEW_SECTION, data['code'], *[
                         data['sections'][section_id]['code'] for section_id in new_sections]))
                
        self._data = data
        return diffs
