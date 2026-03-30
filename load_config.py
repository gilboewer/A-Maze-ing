import sys
from typing import Any


REQUIRED_SETTINGS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}  # noqa: E501
SETTINGS_TYPES = {"WIDTH": "int", "HEIGHT": "int", "ENTRY": "cords",
                  "EXIT": "cords", "OUTPUT_FILE": "str", "PERFECT": "bool"}


class ConfigError(Exception):
    pass


class ConfigFormatError(ConfigError):
    def __init__(self, line_number: int, line: str, msg: str):
        super().__init__(f"Line {line_number} '{line}' - {msg}")


class ConfigParseError(ConfigError):
    def __init__(self, setting: str, value: Any, msg: str):
        super().__init__(f"Invalid value for '{setting}': {value} - {msg}")


class ConfigValueError(ConfigError):
    def __init__(self, setting: str, value: Any, msg: str):
        super().__init__(f"Invalid value for '{setting}': {value} - {msg}")


# TODO: Comments
def read_config(config: dict[str, Any]):
    if len(sys.argv) == 2:
        config_file = sys.argv[1]
    else:
        config_file = "default_config.txt"

    with open(config_file) as cf:
        line_number = 0
        for line in cf:
            line_number += 1
            line = line.strip('\n')
            if ' ' in line or '\t' in line:
                raise ConfigFormatError(line_number, line,
                                        "Line cannot contain spaces")
            if len(line.split('=')) != 2:
                raise ConfigFormatError(line_number, line,
                                        "Line must contain exactly 1 '=' sign")
            setting = line.split('=')[0]
            value = line.split('=')[1]
            if not setting or not value:
                raise ConfigFormatError(line_number, line,
                                        "Missing field(s)")
            config[setting] = value


def parse_config(config: dict[str, Any]):
    if not config.keys() <= SETTINGS_TYPES.keys():
        unknown_settings = config.keys() - SETTINGS_TYPES.keys()
        raise ConfigError(
            f"Unknown setting(s): '{", ".join(unknown_settings)}'")

    for setting, value in config.items():
        config[setting] = convert_value(setting, value)
    return config


def convert_value(setting: str, value: Any) -> Any:
    match SETTINGS_TYPES[setting]:
        case "int":
            try:
                value = int(value)
            except ValueError:
                raise ConfigParseError(setting, value, "Not a valid integer")
        case "cords":
            if len(value.split(',')) != 2:
                raise ConfigParseError(setting, value, "Expected 'x,y'")
            try:
                value = (int(value.split(',')[0]), int(value.split(',')[1]))
            except ValueError:
                raise ConfigParseError(setting, value, "Invalid coordinates")
        case "bool":
            if value == "True":
                value = True
            elif value == "False":
                value = False
            else:
                raise ConfigParseError(setting, value,
                                       "Must be 'True' or 'False'")
    return value


# TODO: Additional settings
def validate_config(config: dict[str, Any]):
    if not REQUIRED_SETTINGS <= config.keys():
        missing_settings = REQUIRED_SETTINGS - set(config.keys())
        raise ConfigError(
            f"Missing setting(s): '{", ".join(missing_settings)}'")

    validate_values(config)


def validate_values(config: dict[str, Any]):
    for setting, value in config.items():
        if setting in ("WIDTH", "HEIGHT"):
            if value <= 0:
                raise ConfigValueError(setting, value,
                                       "Must be a non-zero positive integer")
        if setting in ("Entry", "EXIT"):
            x, y = value
            if x < 0 or y < 0:
                raise ConfigValueError(setting, value,
                                       "Cannot be negative")
            width, height = config["WIDTH"], config["HEIGHT"]
            if x >= width or y >= height:
                raise ConfigValueError(setting, value,
                                       "Coordinates exceed maze bounds"
                                       f" ({width - 1}, {height - 1})")


def load_config() -> dict[str, Any]:
    config = {}
    read_config(config)
    parse_config(config)
    validate_config(config)
    return config
