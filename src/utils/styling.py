# src/utils/styling.py

def stylize_number(n: int) -> str:
    digits = str(n)
    return ''.join(chr(0x1D7EC + int(d)) for d in digits)  # double-struck digits 0–9

def stylize_code(code: str) -> str:
    out: list[str] = []
    for ch in code:
        if 'A' <= ch <= 'Z':
            out.append(chr(0x1D468 + (ord(ch) - ord('A'))))   # italic A–Z
        elif 'a' <= ch <= 'z':
            out.append(chr(0x1D482 + (ord(ch) - ord('a'))))   # italic a–z
        elif '0' <= ch <= '9':
            out.append(chr(0x1D7CE + int(ch)))                # bold digits
        else:
            out.append(ch)
    return ''.join(out)

def style_arguments(*args: int | str):
    styled: list[str] = []
    for arg in args:
        match arg:
            case int():
                styled.append(stylize_number(arg))
            case str() if 1 <= arg.count('-') <= 2:
                styled.append(stylize_code(arg))
            case _:
                styled.append(str(arg))
    return styled

__all__ = ["stylize_number", "stylize_code", "style_arguments"]
