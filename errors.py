from typing import Any


class ConfigError(Exception):
    pass


class ConfigFormatError(ConfigError):
    def __init__(self, line_number: int, line: str, msg: str):
        super().__init__(f"Line {line_number} '{line}'. {msg}")


class ConfigParseError(ConfigError):
    def __init__(self, setting: str, value: str, msg: str):
        super().__init__(f"Invalid value for '{setting}': '{value}'. {msg}")


class ConfigValueError(ConfigError):
    def __init__(self, setting: str, value: Any, msg: str):
        super().__init__(f"Invalid value for '{setting}': '{value}'. {msg}")
