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