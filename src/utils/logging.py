# src/utils/logging.py

import logging
from logging.handlers import RotatingFileHandler

def _is_ascii_printable(ch: str) -> bool:
    return 32 <= ord(ch) <= 126

def normalize_styled_value(text: str) -> str:
    """
    Convert styled math letters/digits to plain ASCII for clean logs.
    Keep ASCII, map — -> -- and → -> ->, drop other symbols/emojis.
    """
    out: list[str] = []
    for c in text:
        # Italic A–Z (U+1D468–U+1D481)
        if '\U0001D468' <= c <= '\U0001D481':
            out.append(chr(ord('A') + (ord(c) - ord('\U0001D468'))))
        # Italic a–z (U+1D482–U+1D49B)
        elif '\U0001D482' <= c <= '\U0001D49B':
            out.append(chr(ord('a') + (ord(c) - ord('\U0001D482'))))
        # Bold digits 0–9 (U+1D7CE–U+1D7D7)
        elif '\U0001D7CE' <= c <= '\U0001D7D7':
            out.append(chr(ord('0') + (ord(c) - ord('\U0001D7CE'))))
        # Double-struck digits 0–9 (U+1D7EC–U+1D7F5)
        elif '\U0001D7EC' <= c <= '\U0001D7F5':
            out.append(chr(ord('0') + (ord(c) - ord('\U0001D7EC'))))
        # Friendly mappings for common symbols
        elif c == '—':
            out.extend('--')
        elif c == '→':
            out.extend('->')
        # Keep ASCII printable as-is
        elif _is_ascii_printable(c):
            out.append(c)
        # Drop everything else (emoji/zero-width/etc.)
        else:
            continue
    return ''.join(out).strip()

def log(message: str) -> None:
    logging.info(normalize_styled_value(message))

def print_and_log(message: str) -> None:
    print(message)
    log(message)

def setup_logging(
    *,
    level: int = logging.INFO,
    logfile: str | None = "output/scraper.log",
    to_console: bool = True,
    rotating: bool = True,
    max_bytes: int = 1_000_000,
    backup_count: int = 3,
    fmt: str = "%(asctime)s [%(levelname)s] %(message)s",
    datefmt: str = "%H:%M:%S",
) -> None:
    """
    Call once at startup. Creates console/file handlers as requested.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # avoid duplicate handlers if called twice
    if logger.handlers:
        return

    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    if logfile:
        if rotating:
            fh = RotatingFileHandler(logfile, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
        else:
            fh = logging.FileHandler(logfile, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if to_console:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

__all__ = ["normalize_styled_value", "log", "print_and_log", "setup_logging"]
