from src.scraper import fetch_sections_by_course_labels
import requests


def test_sections_by_course_labels():
    session = requests.Session()
    # courses with sections
    non_empty_sections = fetch_sections_by_course_labels(session, ["ACC-230", "BAD-260"])

    assert len(non_empty_sections) > 0, "No sections fetched for the provided course labels"

    # courses without sections
    empty_sections = fetch_sections_by_course_labels(session, ["MATH-024", "MATH-100SI"])
    assert len(empty_sections) == 0, "Sections should be empty for courses without sections"
