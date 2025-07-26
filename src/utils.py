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
