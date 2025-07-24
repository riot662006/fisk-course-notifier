from src.scraper import load_courses, save_courses
from src.course import Course

ex_course = Course({
    "Id": 101,
    "MatchingSectionIds": ["1234", "5678"],
    "Title": "Intro to Computing",
    "SubjectCode": "CSCI",
    "Number": "101"
})


def test_course_to_dict():
    result = ex_course.to_dict()
    assert result["courseId"] == 101
    assert result["sectionIds"] == ["1234", "5678"]
    assert result["title"] == "Intro to Computing"
    assert result["subjectCode"] == "CSCI"
    assert result["subjectNumber"] == "101"


def test_get_course_label():
    label = ex_course.get_course_label()
    assert label == "CSCI-101"


def test_save_n_load_courses():
    path = 'output/tmp'
    save_courses([ex_course], path)

    courses = list(load_courses(path).values())

    assert courses == [
        ex_course.to_dict()], "Saved course data does not match expected output."


def test_save_n_load_courses_doesnt_exist():
    path = 'output/asdfghjkzxcvbnwertyu1234567890'

    try:
        load_courses(path)
        raise RuntimeError(
            "Expected an error when trying to save to a non-existent path, but none was raised."
        )
    except FileNotFoundError:
        pass

    path = 'output/tmp'
    with open(path, 'w') as f:
        f.write("This is not a valid JSON file.")

    try:
        load_courses(path)
        raise RuntimeError(
            "Expected an error when trying to load a corrupted JSON file, but none was raised."
        )
    except ValueError as e:
        assert str(
            e) == f"Could not load courses from {path}. File may be missing or corrupted."
