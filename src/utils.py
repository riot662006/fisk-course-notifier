import logging


def stylize_number(n: int) -> str:
    digits = str(n)
    return ''.join(chr(0x1D7EC + int(d)) for d in digits)


def style_arguments(*args: int | str):
    styled_args: list[str] = []

    for arg in args:
        match arg:
            case int():
                styled_args.append(stylize_number(arg))
            case code if 1 <= code.count('-') <= 2:
                styled_args.append(stylize_code(arg))
            case _:
                styled_args.append(arg)

    return styled_args


def stylize_code(code: str) -> str:
    result: list[str] = []

    for char in code:
        if 'A' <= char <= 'Z':
            # Italic capital A-Z: U+1D468
            result.append(chr(0x1D468 + ord(char) - ord('A')))
        elif 'a' <= char <= 'z':
            # Italic lowercase a-z: U+1D482
            result.append(chr(0x1D482 + ord(char) - ord('a')))
        elif '0' <= char <= '9':
            # Bold digits: U+1D7CE
            result.append(chr(0x1D7CE + int(char)))
        else:
            result.append(char)

    return ''.join(result)


def is_ascii_printable(c: str) -> bool:
    return 32 <= ord(c) <= 126


def normalize_styled_value(text: str) -> str:
    normalized: list[str] = []

    for c in text:
        # Revert stylized uppercase A-Z (italic A: U+1D468)
        if '\U0001D468' <= c <= '\U0001D481':
            normalized.append(chr(ord('A') + ord(c) - ord('\U0001D468')))
        # Revert stylized lowercase a-z (italic a: U+1D482)
        elif '\U0001D482' <= c <= '\U0001D49B':
            normalized.append(chr(ord('a') + ord(c) - ord('\U0001D482')))
        # Revert bold digits 0-9: U+1D7CE
        elif '\U0001D7CE' <= c <= '\U0001D7D7':
            normalized.append(chr(ord('0') + ord(c) - ord('\U0001D7CE')))
        # Revert double-struck digits 0-9: U+1D7EC
        elif '\U0001D7EC' <= c <= '\U0001D7F5':
            normalized.append(chr(ord('0') + ord(c) - ord('\U0001D7EC')))
        # Keep normal printable characters
        elif is_ascii_printable(c):
            normalized.append(c)
        # Keep em dash as --
        elif c == '—':
            normalized.extend('--')
        elif c == '→':
            normalized.extend('->')
        # Skip emoji/symbols
        else:
            continue

    return ''.join(normalized).strip()


def log(message: str):
    safe = normalize_styled_value(message)
    logging.info(safe)


def print_and_log(message: str):
    print(message)
    log(message)
