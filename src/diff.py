from enum import Enum


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
        match self._code:
            case DiffCode.NEW_SECTION:
                course_code, section_codes, free_seats = self._args
                return f"🆕 New section {section_codes} just popped up for {course_code}! {free_seats} avaliable seats. Don’t miss it!"

            case DiffCode.SEATS_BECAME_AVAILABLE:
                section_code, free_seats = self._args
                return f"✅ Section {section_code} has open seats now. {free_seats} left! Be quick!!!!"

            case DiffCode.SEATS_BECAME_UNAVAILABLE:
                section_code = self._args
                return f"❌ Section {section_code} is now full. Somebody beat you to it 😢"

            case DiffCode.SEATS_DROPPED:
                section_code, seats = self._args
                return f"⚠️ Only {seats} left in section {section_code}! Seats going fast!"

            case DiffCode.SEATS_ROSE:
                section_code, seats = self._args
                return f"🔼 More seats just opened up in section {section_code} — back above {seats}. Suspicious no?"

            case DiffCode.PROFESSOR_CHANGED:
                section_code, old_prof, new_prof = self._args
                return f"👨‍🏫 Section {section_code} has a new professor: {old_prof} → {new_prof}"

            case DiffCode.FIRST_FETCH:
                course_code, = self._args
                return f"🆕 First time tracking course {course_code} — now watching."

            case DiffCode.SECTION_REMOVED:
                course_code, section_code = self._args
                return f"🚫 Section {section_code} in {course_code} has been removed. No longer tracking."

            case _:
                return f"❓ Unknown diff code: {self._code.value}"
