# src/core/scraper_legacy.py

from typing import Any

import asyncio
import logging
import json
import hashlib
import time
import threading
from concurrent.futures import ThreadPoolExecutor

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .base_scraper import create_driver, send_notification

# Thread lock to prevent race conditions
file_lock = threading.Lock()


def get_course_section_table(course_id: str):
    """Scrape course section table for a given course ID."""
    logging.info(f"Starting scraping for course: {course_id}")

    # Ensure headless mode is used
    driver = create_driver(f"Search?keyword={course_id}", headless=True)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, "collapsible-1-collapseBody")))
        courses_HTML = driver.find_element(
            # type: ignore
            By.ID, "course-results").find_elements(By.CLASS_NAME, "esg-section--margin-top")

        if not courses_HTML:
            logging.warning(f"No courses found for {course_id}")
            return None

        course_HTML = courses_HTML[0]
        collapsible = course_HTML.find_element(  # type: ignore
            By.TAG_NAME, "collapsible-group")
        collapsible_btn = collapsible.find_element(  # type: ignore
            By.CLASS_NAME, "esg-collapsible-group__toggle")
        collapsible_btn.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@data-bind='foreach: TermsAndSections']//div"))
        )

        tables_HTML = collapsible.find_element(By.XPATH, "//div[@data-bind='foreach: TermsAndSections']").find_element(  # type: ignore
            By.XPATH, "//h4[contains(text(), 'Fall 2025')]"
        ).find_element(By.XPATH, "./following-sibling::ul").find_elements(By.TAG_NAME, "table")

        table_data = [[cell.text.strip() for cell in table.find_elements(  # type: ignore
            By.TAG_NAME, "tr")[1].find_elements(By.TAG_NAME, "td")] for table in tables_HTML]

        logging.info(
            f"Scraping successful for {course_id}, extracted {len(table_data)} sections.")
        return {course_id: table_data}

    except Exception as e:
        logging.error(f"Error while scraping {course_id}: {e}")
        return None

    finally:
        driver.quit()


def generate_hash(data: dict[str, Any]) -> str:
    """Generate a hash value for a given data structure."""
    data_string = json.dumps(
        data, sort_keys=True)  # Convert to JSON string format
    # Generate SHA-256 hash
    return hashlib.sha256(data_string.encode('utf-8')).hexdigest()


def save_results_to_json(results: list[dict[str, list[list[str]]] | None], filename: str = "output/course_data.json"):
    """Safely save scraped results to a JSON file."""
    with file_lock:
        should_update = False

        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        for result in results:
            if result:
                for key, value in result.items():
                    current_hash = generate_hash(
                        data.get(key, []))  # type: ignore
                    new_hash = generate_hash(value)  # type: ignore

                    if current_hash != new_hash:
                        logging.info(f"New data found for {key}")
                        data[key] = value
                        should_update = True

        if (should_update):
            push = send_notification("COLLEAGUE SCRAPER",  # type: ignore
                                     "New content!!! Check logs for details!!!")
            logging.info(f"Push sent: {push}")
            logging.info(f"Saving updated data to {filename}")
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)


async def scrape_courses_async(course_codes: list[str]):
    """Runs multiple scraping tasks asynchronously."""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks = [loop.run_in_executor(
            executor, get_course_section_table, course_code) for course_code in course_codes]
        results = await asyncio.gather(*tasks)
        save_results_to_json(results)


def scrape_courses(course_codes: list[str]):
    """Main function to scrape courses."""

    try:
        while True:
            # Run the scraping function
            asyncio.run(scrape_courses_async(course_codes))
            logging.info("Waiting 1 minute before next scrape...")
            time.sleep(60)  # Wait 60 seconds before the next run
    except KeyboardInterrupt:
        logging.info("Scraper interrupted by user. Exiting gracefully.")
        print("\nScraper stopped.")
