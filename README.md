# Fisk Course Notifier

> **✍️ Motivation:** I was often late to register for classes because the current system doesn’t notify students when new course sections open up. To solve this, I built my own notification system that checks for changes and alerts me instantly — making sure I never miss an opportunity again.

## 🚀 What’s New in This Version?

- **Direct API Scraping:**  
  No more brittle Selenium scraping! The scraper now talks directly to Fisk’s Colleague Self-Service API for lightning-fast, reliable data.
- **Modern Data Model:**  
  All course and section data is structured and diffed for changes—no more manual table parsing.
- **Change Detection & Smart Alerts:**  
  Get notified only when something meaningful happens: new sections, seat availability, professor changes, and more.
- **Pushbullet Integration:**  
  Instant phone or desktop notifications for important updates.
- **Robust Logging:**  
  All events and errors are logged to `output/scraper.log` for easy troubleshooting.
- **Configurable Monitoring:**  
  Easily choose which courses to watch and how often to check.

## 📁 Project Structure

- [`main.py`](main.py): Starting point
- [`src/scraper.py`](src/scraper.py): Main watcher loop, API fetch, diffing, and notification logic.
- [`src/course.py`](src/course.py): Course and section data model, change tracking.
- [`src/diff.py`](src/diff.py): Change types and pretty message formatting.
- [`src/utils.py`](src/utils.py): Logging, stylized output, and helpers.

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
3. **Install Browser Driver (Only for Legacy Version)**

   - Instructions below and the browser used in this repo is for **Chrome**. Make sure to change driver if using different browser driver.
   - Check your Chrome Version (goto `chrome://settings/help`).
   - Download the matching ChromeDriver from [https://sites.google.com/chromium.org/driver](https://sites.google.com/chromium.org/driver) e.g. chromedriver_win32.zip
   - Extract and add folder that has the `chromedriver.exe` file to PATH environment variables.

4. **Configure Pushbullet:**
   - Create a .env file with your Pushbullet API key:

## Run the scraper:

```sh
python main.py [--legacy] [course_codes ...]
```

- The script will fetch the latest data, compare with previous results, and notify you of any changes.
- All changes and errors are logged to `output/scraper.log`.
- Data is saved to `output/course_data.json` for persistence.

## 🆕 Example Notification Types

- **New Section Added:**  
  🆕 New NSCI-290-03! 25 seats!
- **Seats Became Available:**  
  ✅ NSCI-290-03 has 5 open! Jump in!
- **Section Removed:**  
  🚫 NSCI-290-04 removed.
- **Professor Changed:**  
  👨‍🏫 NSCI-290-03: Prof changed Dr. Smith → Dr. Jones

## Requirements

- Python 3.11+
- Pushbullet account (for notifications)
- [FOR LEGACY VERSION] Chrome browser and [ChromeDriver](https://chromedriver.chromium.org/downloads) _(can work with any browser and driver)_
- See [`requirements.txt`](requirements.txt) for Python packages.

## 🛣️ Next Steps

The current notifier is fully API-based and significantly more reliable than the old Selenium version. That said, there's still room to grow:

### 💻 Web Dashboard Interface

- Build a lightweight **Next.js** or **Flask** UI to manage watched courses.
- Allow users to:
  - View current course/section statuses.
  - Add/remove courses to track.
  - View recent change logs and diffs in a friendly format.

### 🔔 Smarter Notification Controls

- Let users choose notification **channels** (Pushbullet, SMS, email).
- Add **cooldown settings** to avoid spamming (e.g., “only notify if seats dropped to 5 or fewer”).
- Group multiple diffs into **summarized alerts**.

### 🧠 Historical Trends & Analytics

- Store snapshots of course data over time.
- Show trends like:
  - Most volatile sections
  - Frequent seat drops or professor switches
  - Seat availability heatmaps per hour/day

### 📤 Shareable Watchlists

- Let users export/import course watchlists.
- Generate links to share watchlists with friends or teammates (JSON or encoded URLs).

### 🧪 Improved Testing & Dev Experience

- Add tests for diff generation, silent diffs, and stylization logic.
- Mock API fetches for fast local testing.
- Improve CLI/dev tooling (e.g., `--watchlist`, `--log-level`, etc.)

## 📄⚠️ License & Disclaimer

- This project is intended for **personal and educational** use only.
- It is **not** affiliated with or endorsed by Fisk University or Ellucian.
- Please **use responsibly** and in accordance with your institution’s policies.

Note: This scraper is tailored for Fisk University's Colleague Self-Service portal and may require adaptation for other institutions or portals.

> 📌 If you're interested in helping me expand this project, feel free to reach out or open an issue!
