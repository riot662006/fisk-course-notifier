from enum import Enum


class DiffCode(Enum):
    NEW_SECTION = "NEW_SECTION"
    SEATS_BECAME_AVAILABLE = "SEATS_BECAME_AVAILABLE"
    SEATS_BECAME_UNAVAILABLE = "SEATS_BECAME_UNAVAILABLE"
    SEATS_DROPPED = "SEATS_DROPPED_BELOW_THRESHOLD"
    SEATS_ROSE = "SEATS_ROSE_ABOVE_THRESHOLD"
    PROFESSOR_CHANGED = "PROFESSOR_CHANGED"


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

            case _:
                return f"❓ Unknown diff code: {self._code.value}"
