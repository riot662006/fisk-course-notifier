from enum import Enum


class DiffCode(Enum):
    NEW_SECTION = "NEW_SECTION"


class Diff:
    def __init__(self, code: DiffCode, *args: str):
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
                course_code, *section_codes = self._args

                if len(section_codes) == 1:
                    sections_text = f"section {section_codes[0]}"
                else:
                    sections_text = f"sections ({", ".join(section_codes)})"
                    
                return f"➕ New {sections_text} added to course {course_code}."
            case _:
                return f"❓ Unknown diff code: {self._code.value}"
