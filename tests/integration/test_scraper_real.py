import pytest

from src.scraper import watch_courses


@pytest.mark.integration
def test_scraper_request():
    watch_courses(["NSCI-290"])
