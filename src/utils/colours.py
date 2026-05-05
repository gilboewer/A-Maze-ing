"""ANSI color codes for terminal rendering."""

COLORS = {
    "white": "\033[37m",
    "red": "\033[31m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "yellow": "\033[33m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}

RESET = "\033[0m"

COLOR_NAMES = list(COLORS.keys())


def colorize(text: str, color: str) -> str:
    """
    Applies ANSI color to text.

    Args:
        text (str): Text to colorize.
        color (str): Color name from COLORS dict.

    Returns:
        str: Colored text with reset code.
    """
    if color in COLORS:
        return COLORS[color] + text + RESET
    return text
