import argparse
from src.scraper_legacy import scrape_courses as watch_courses_legacy
from src.scraper import watch_courses


def main():
    parser = argparse.ArgumentParser(
        description="📡 Monitor course availability and notify on changes."
    )

    parser.add_argument(
        "course_codes",
        nargs="*",
        help="List of course codes like CSCI-291 or NSCI-360"
    )

    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Run legacy notifier"
    )

    args = parser.parse_args()

    if not args.course_codes:
        print("⚠️ No course codes provided.")
        parser.print_usage()
        return

    course_codes = [code.upper() for code in args.course_codes]

    if args.legacy:
        print("🕰️ Running legacy notifier...")
        watch_courses_legacy(course_codes)
    else:
        print("🚀 Running latest notifier...")
        watch_courses(course_codes)


if __name__ == "__main__":
    main()
