import pytest

from src import watch_courses


@pytest.mark.integration
def test_scraper_request():
    watch_courses(["NSCI-290"])
