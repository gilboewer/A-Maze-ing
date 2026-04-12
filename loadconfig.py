import sys
from typing import Any

from errors import ConfigFormatError, ConfigParseError


def read_config(config: dict):
    if len(sys.argv) == 2:
        config_file = sys.argv[1]
    else:
        config_file = "config.txt"

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


def parse_config(config: dict):
    for setting, value in config.items():
        config[setting] = parse_value(setting, value)
    return config


def parse_value(setting: str, value: str) -> Any:
    if len(value.split(',')) > 2:
        raise ConfigParseError(setting, value, "Not a valid value format")
    elif len(value.split(',')) == 2:
        try:
            return int(value.split(',')[0]), int(value.split(',')[1])
        except ValueError:
            raise ConfigParseError(setting, value,
                                   "2 valid integers expected for cords")
    else:
        try:
            return int(value)
        except ValueError:
            pass
        if value == "True":
            return True
        if value == "False":
            return False
        return value


def load_config() -> dict:
    config = {}
    read_config(config)
    parse_config(config)
    return config
