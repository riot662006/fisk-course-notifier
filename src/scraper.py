from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
import json
from urllib.parse import urljoin

from course import Course
from custom_types import SectionsSearchCriteria
from section import Section

BASE_URL = "https://fisk-ss.colleague.elluciancloud.com/Student/Courses/"


def create_driver(url, cookies={}, headless=False):
    # Initialize the Selenium WebDriver with necessary options
    options = Options()

    if headless:
        options.add_argument('--headless=new')

    # Fix network crashes & timeout issues
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument(
        "--disable-component-extensions-with-background-pages")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Set the cookies from the `requests` response
    for cookie_name, cookie_value in cookies.items():
        driver.add_cookie({'name': cookie_name, 'value': cookie_value})

    # After setting the cookies, refresh the page in Selenium to apply them
    driver.refresh()

    return driver


def throw_bad_response(response: requests.Response):
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    return response


def fetch_courses(session, search_criteria):
    response = session.post(
        urljoin(BASE_URL, "PostSearchCriteria"),
        headers={
            'content-type': 'application/json, charset=UTF-8',
        },
        data=json.dumps(search_criteria)
    )
    throw_bad_response(response)

    courses = response.json()["Courses"]

    return [
        Course(
            course
        )
        for course in courses
    ]


def fetch_sections(session: requests.Session, search_criteria: SectionsSearchCriteria):
    response = session.post(
        urljoin(BASE_URL, "Sections"),
        headers={
            'content-type': 'application/json, charset=UTF-8',
        },
        data=json.dumps(search_criteria)
    )
    throw_bad_response(response)

    term_and_sections = response.json(
    )["SectionsRetrieved"]["TermsAndSections"]

    return [
        Section(section_data)

        for term_and_section in term_and_sections
        for section_data in term_and_section['Sections']
    ]


if __name__ == "__main__":
    session = requests.Session()
    courses = fetch_courses(session, search_criteria={"terms": ["2025FA", "2025SU"], "keywordComponents": [
        {"subject": "CSCI", "courseNumber": "", "section": "", "synonym": ""},
        {"subject": "ART", "courseNumber": "", "section": "", "synonym": ""}
    ], })
    print(f"Found {len(courses)} courses:")
    pprint(courses)

    sections = fetch_sections(
        session, courses[0].get_sections_search_criteria())
    print(f"\n{courses[0].title} sections:")
    pprint(sections)
