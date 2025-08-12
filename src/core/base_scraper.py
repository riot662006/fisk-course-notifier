# src/core/base_scraper.py

from dotenv import load_dotenv
from pushbullet import Pushbullet  # type: ignore
from typing import Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin

import json
import logging
import os
import requests

BASE_URL = "https://fisk-ss.colleague.elluciancloud.com/Student/Courses/"

# Configure Logging
logging.basicConfig(filename="output/scraper.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Load pushBullet api variables for messages
load_dotenv()
PUSH_BULLET_API_KEY = os.getenv("PUSH_BULLET_API_KEY")

pb = Pushbullet(PUSH_BULLET_API_KEY)


def create_driver(path: str, headless: bool = False):
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
    driver.get(urljoin(BASE_URL, path))

    # After setting the cookies, refresh the page in Selenium to apply them
    driver.refresh()

    return driver


def fetch(session: requests.Session, path: str, data: dict[str, Any]) -> dict[str, Any]:
    response = session.post(
        urljoin(BASE_URL, path),
        headers={
            'content-type': 'application/json, charset=UTF-8',
        },
        data=json.dumps(data)
    )

    response.raise_for_status()
    return response.json()


def send_notification(title: str, body: str):
    pb.push_note(title, body)  # type: ignore
