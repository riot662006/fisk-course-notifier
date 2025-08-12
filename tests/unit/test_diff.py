from typing import Optional
from src.custom_types import CourseData, SectionData
from src.course import Course
from src.diff import Diff, DiffCode


def course_data_factory(code: str = "CSCI-101", id: str = "123", sections: Optional[dict[str, SectionData]] = None) -> CourseData:
    if sections is None:
        sections = {}
    return {
        "id": id,
        "code": code,
        "sections": sections,
        "fetch_timestamp": 0
    }


def section(code: str, free_seats: int = 0, professor: str = "") -> SectionData:
    return {
        "code": code,
        "free_seats": free_seats,
        "professor": professor
    }


def test_no_diff_when_same_data():
    data = course_data_factory(sections={
        "s1": section("001")
    })
    course = Course(data.copy())
    diffs = course.update_data(data.copy())

    assert diffs == [], "Expected no diffs when data is unchanged"


def test_new_section_diff_single():
    old_data = course_data_factory(sections={
        "s1": section("001")
    })
    new_data = course_data_factory(sections={
        "s1": section("001"),
        "s2": section("002")
    })

    course = Course(old_data)
    diffs = course.update_data(new_data)

    assert len(diffs) == 1
    assert diffs[0].code == DiffCode.NEW_SECTION
    assert "002" in diffs[0].get_message()


def test_new_section_diff_multiple():
    old_data = course_data_factory(sections={
        "s1": section("001")
    })
    new_data = course_data_factory(sections={
        "s1": section("001"),
        "s2": section("002"),
        "s3": section("003")
    })

    course = Course(old_data)
    diffs = course.update_data(new_data)

    assert len(diffs) == 1
    assert diffs[0].code == DiffCode.NEW_SECTION
    assert "002" in diffs[0].get_message()
    assert "003" in diffs[0].get_message()
    assert "sections" in diffs[0].get_message()


def test_diff_repr_truncation():
    diff = Diff(DiffCode.NEW_SECTION, "CSCI-101", "001", "002", "003")
    r = repr(diff)
    assert r.startswith("<Diff object - [")
    assert len(r) < 80
