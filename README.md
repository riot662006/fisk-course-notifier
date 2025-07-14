# Fisk Course Notifier
> **✍️ Motivation:** I was often late to register for classes because the current system doesn’t notify students when new course sections open up. To solve this, I built my own notification system that checks for changes and alerts me instantly — making sure I never miss an opportunity again.

This project automates the scraping and monitoring of course section data from Fisk University's Colleague Self-Service portal. It uses Selenium for browser automation, BeautifulSoup for HTML parsing, and Pushbullet for notifications.

## 🚀 Features

- Scrapes course section tables for specified courses.
- Monitors for changes and sends Pushbullet notifications when new data is found.
- Supports asynchronous scraping for multiple courses.
- Includes experiments for direct API requests and data extraction.

## 📁 Project Structure

- [`main.py`](main.py): Main script for scraping and monitoring courses.
- [`src/scraper.py`](src/scraper.py): Selenium driver setup and utilities.

Generated files: 
- [`output/course_data.json`](output/course_data.json): Stores scraped course data.
- [`output/scraper.log`](output/scraper.log): Logging output.

## ⚙️ Setup

1. **Set up virtual environment:**
    ```sh
    python -m venv .venv

    # Windows
    .venv\Scripts\activate

    # MacOs / Linux
    source .venv/bin/activate
    ```
    This activates the virtual environment and should look like `(venv) directory/of/your/project>`
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Install Browser Driver**
    - Instructions below and the browser used in this repo is for **Chrome**. Make sure to change driver if using different browser driver. 
    - Check your Chrome Version (goto `chrome://settings/help`).
    - Download the matching ChromeDriver from [https://sites.google.com/chromium.org/driver](https://sites.google.com/chromium.org/driver) e.g. chromedriver_win32.zip
    - Extract and add folder that has the `chromedriver.exe` file to PATH environment variables.

4. **Configure Pushbullet:**
    - Create a .env file with your Pushbullet API key:

5. **Update Courses to Scrape**
    - Courses that are scraped are defined in `main.py` [here](main.py#L30-31)

## Run the scraper:
```sh
python main.py
```

- The scraper runs in a loop, checking for updates **every minute**.
- When new course data is detected, a Pushbullet notification is sent.
- Scraped data is saved to ``course_data.json``.
- Logs are saved in ``scraper.log``

## Requirements
- Python 3.11+
- Chrome browser and [ChromeDriver](https://chromedriver.chromium.org/downloads) *(can work with any browser and driver)*
- See [`requirements.txt`](requirements.txt) for Python packages.
## 🛣️ Next Steps

The current scraper uses Selenium-based browser automation to interact with Fisk's course portal, but several improvements are planned:

### 🔄 Transition from Selenium to Direct API Calls
- Investigate and reverse-engineer the network requests made by Fisk's Colleague Self-Service to retrieve course data directly.
- Replace the brittle DOM scraping logic with reliable, faster `requests`-based API calls.
- Improve performance and reduce resource usage (headless browser no longer needed).

### ☁️ Web Service Hosting
- Package the scraper as a lightweight server using **Flask** or **FastAPI**.
- Host it (e.g., on Render, Railway, or Fly.io) to allow:
  - On-demand scraping (triggered via HTTP request)
  - Scheduled scraping using external schedulers or internal cron jobs
  - User-specific phone pings or alerts (eventually tied to course interest)

### 🛎️ Push Notifications Customization
- Extend Pushbullet integration to:
  - Allow user-specific keys
  - Customize messages and frequency
  - Integrate with alternative services like Twilio SMS, email, or Telegram

### 📦 Codebase Refinement
- Isolate parsing and scraping logic into cleaner modules.
- Add better error handling and retries for flaky selectors.
- Write tests for the hash check and data comparison logic.

> 📌 If you're interested in collaborating or testing early versions of the API-based implementation, feel free to reach out or open an issue!

## 📄⚠️ License & Disclaimer
- This project is intended for **personal and educational** use only.  
- It is **not** affiliated with or endorsed by Fisk University or Ellucian.  
- Please **use responsibly** and in accordance with your institution’s policies.

Note: This scraper is tailored for Fisk University's Colleague Self-Service portal and may require adaptation for other institutions or portals.
