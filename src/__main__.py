# src/__main__.py

import argparse
import sys

from . import watch_courses, watch_courses_legacy


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="fisk-course-notifier",
        description="📡 Monitor course availability and notify on changes.",
    )
    parser.add_argument(
        "course_codes",
        nargs="*",
        help="Course codes like CSCI-291 or NSCI-360 (space-separated).",
    )
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Run legacy Selenium-based notifier (not recommended).",
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=10,
        help="Polling interval in seconds (default: 10).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    if not args.course_codes:
        print("⚠️ No course codes provided.")
        print(
            "Usage: python -m src [--legacy] [--interval SECONDS] COURSE_CODE ...")
        return 2  # typical 'bad usage' exit code

    course_codes = [code.upper() for code in args.course_codes]

    if args.legacy:
        print("🕰️ Running legacy notifier...")
        watch_courses_legacy(course_codes)
    else:
        print("🚀 Running latest notifier...")
        watch_courses(course_codes, poll_interval=args.interval)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
