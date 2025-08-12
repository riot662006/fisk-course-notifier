# src/models/diff.py

from enum import Enum

from src.utils import style_arguments


class DiffCode(Enum):
    NEW_SECTION = ("NEW_SECTION", False)
    SEATS_BECAME_AVAILABLE = ("SEATS_BECAME_AVAILABLE", False)
    SEATS_BECAME_UNAVAILABLE = ("SEATS_BECAME_UNAVAILABLE", False)
    SEATS_DROPPED = ("SEATS_DROPPED_BELOW_THRESHOLD", False)
    SEATS_ROSE = ("SEATS_ROSE_ABOVE_THRESHOLD", False)
    PROFESSOR_CHANGED = ("PROFESSOR_CHANGED", False)

    # Silent diffs
    FIRST_FETCH = ("FIRST_FETCH", True)
    SECTION_REMOVED = ("SECTION_REMOVED", True)

    def __init__(self, value: str, is_silent: bool):
        self._value_ = value  # override Enum's internal value
        self.is_silent = is_silent


class Diff:
    def __init__(self, code: DiffCode, *args: str | int):
        self._code = code
        self._args = args

    def __repr__(self):
        msg = self.get_message()
        preview = msg[:40] + "..." if len(msg) > 10 else msg

        return f"<Diff object - [{preview}]"

    @property
    def code(self):
        return self._code

    def is_silent(self):
        return self.code.is_silent

    def get_message(self) -> str:
        args = style_arguments(*self._args)

        match self._code:
            case DiffCode.NEW_SECTION:
                section_code, seats = args
                return f"🆕  New {section_code}! {seats} seats!"

            case DiffCode.SEATS_BECAME_AVAILABLE:
                section_code, seats = args
                return f"✅  {section_code} has {seats} open! Jump in!"

            case DiffCode.SEATS_BECAME_UNAVAILABLE:
                section_code, = args
                return f"❌  {section_code} is full! Too slow 😢"

            case DiffCode.SEATS_DROPPED:
                section_code, seats = args
                return f"⚠️  {section_code} down to {seats} seats!"

            case DiffCode.SEATS_ROSE:
                section_code, seats = args
                return f"🔼  {section_code} back up — {seats} seats now."

            case DiffCode.PROFESSOR_CHANGED:
                section_code, old, new = args
                return f"👨‍🏫  {section_code}: Prof changed {old} → {new}"

            case DiffCode.FIRST_FETCH:
                course_code, = args
                return f"👀  Now watching {course_code}."

            case DiffCode.SECTION_REMOVED:
                section_code, = args
                return f"🚫  {section_code} removed."

            case _:
                return f"❓  Unknown diff: {self._code.value}"

