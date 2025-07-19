from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import requests
import json
from urllib.parse import urljoin, urlparse, urlencode

from bs4 import BeautifulSoup

BASE_URL = "https://fisk-ss.colleague.elluciancloud.com/Student/Courses/"
CSRF_COOKIE_NAME = '.ColleagueSelfServiceAntiforgery'


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
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)

    return response


def get_token_from_home_response(response: requests.Response):
    soup = BeautifulSoup(response.text, 'html.parser')
    token_input = soup.find('input', {'name': '__RequestVerificationToken'})

    if token_input:
        return token_input['value']
    else:
        raise ValueError("CSRF token not found in the response HTML.")


def get_request_headers(response: requests.Response):
    csrf = response.cookies.get(CSRF_COOKIE_NAME)
    token = get_token_from_home_response(response)

    return {
        '__isguestuser': 'true',
        '__requestverificationtoken': token,
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json, charset=UTF-8',
        'origin': 'https://fisk-ss.colleague.elluciancloud.com',
        'priority': 'u=1, i',
        'referer': response.url,
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Opera GX";v="119"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': f'{CSRF_COOKIE_NAME}={csrf};',
    }


def fetch_request_headers(session: requests.Session, url: str):
    home_response = throw_bad_response(session.get(url))
    headers = get_request_headers(home_response)

    return headers


def fetch_courses(session, headers, search_criteria):
    response = session.post(
        urljoin(BASE_URL, "PostSearchCriteria"),
        headers=headers,
        data=json.dumps(search_criteria)
    )
    throw_bad_response(response)

    return response.json()["Courses"]


if __name__ == "__main__":
    session = requests.Session()
    headers = fetch_request_headers(session, BASE_URL)

    courses = fetch_courses(session, headers, search_criteria={"terms": ["2025FA"], "keywordComponents": [
        {"subject": "CSCI", "courseNumber": "", "section": "", "synonym": ""},
        {"subject": "ART", "courseNumber": "", "section": "", "synonym": ""}
    ], })

    print(f"Found {len(courses)} courses.")
    pprint(courses)
