# src/core/__init__.py

from .scraper import watch_courses
from .scraper_legacy import scrape_courses as watch_courses_legacy

__all__ = ["watch_courses", "watch_courses_legacy"]
