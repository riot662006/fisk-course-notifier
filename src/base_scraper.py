from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://fisk-ss.colleague.elluciancloud.com/Student/Courses/"


def create_driver(url: str, cookies: dict[str, str] = {}, headless: bool = False):
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
        driver.add_cookie(  # type: ignore
            {'name': cookie_name, 'value': cookie_value})

    # After setting the cookies, refresh the page in Selenium to apply them
    driver.refresh()

    return driver
