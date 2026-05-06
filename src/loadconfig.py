import sys
from typing import Any
from .errors import ConfigFormatError, ConfigParseError, ConfigError


def read_config(config_file: str, config: dict) -> None:
    """
    Reads configuration from a file and populates the config dictionary.

    Args:
        config_file (str): Path to the configuration file.
        config (dict): Dictionary to populate with configuration settings.

    Raises:
        ConfigFormatError: If the file format is invalid.
    """
    with open(config_file) as cf:
        line_number = 0
        for line in cf:
            line_number += 1
            if line.strip()[0] == '#':
                continue
            line = line.strip('\n')
            if len(line.split('=')) != 2:
                raise ConfigFormatError(line_number, line,
                                        "Line must contain exactly 1 '=' sign")
            if ' ' in line or '\t' in line:
                raise ConfigFormatError(line_number, line,
                                        "Line cannot contain spaces")
            setting = line.split('=')[0]
            value = line.split('=')[1]
            if not setting or not value:
                raise ConfigFormatError(line_number, line,
                                        "Missing field(s)")
            config[setting] = value


def parse_config(config: dict) -> None:
    """
    Parses string values in the config dictionary into appropriate types.

    Args:
        config (dict): Configuration dictionary with string values.

    Raises:
        ConfigParseError: If a value cannot be parsed.
    """
    for setting, value in config.items():
        config[setting] = parse_value(setting, value)


def parse_value(setting: str, value: str) -> Any:
    """
    Parses a single configuration value into the appropriate type.

    Args:
        setting (str): The configuration setting name.
        value (str): The string value to parse.

    Returns:
        Any: The parsed value (int, bool, str, or tuple).

    Raises:
        ConfigParseError: If the value format is invalid.
    """
    if len(value.split(',')) > 2:
        raise ConfigParseError(setting, value, "Not a valid value format")
    elif len(value.split(',')) == 2:
        try:
            return int(value.split(',')[1]), int(value.split(',')[0])
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
    """
    Loads configuration from file or default.

    Returns:
        dict: Parsed configuration dictionary.

    Raises:
        ConfigError: If config file is not found or invalid.
    """
    config: dict = {}
    if len(sys.argv) == 2:
        config_file = sys.argv[1]
    else:
        config_file = "config.txt"
    try:
        read_config(config_file, config)
    except FileNotFoundError:
        raise ConfigError(f"Config file '{config_file}' not found")
    parse_config(config)
    return config
