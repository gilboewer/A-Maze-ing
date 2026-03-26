import sys
from typing import Any


class ConfigError(Exception):
    pass


class ConfigFormatError(ConfigError):
    def __init__(self, line: str, msg: str):
        super().__init__(f"'{line}' - {msg}")


REQUIRED_SETTINGS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}  # noqa: E501
SETTINGS_TYPES = {"WIDTH": "int", "HEIGHT": "int", "ENTRY": "cords",
                  "EXIT": "cords", "OUTPUT_FILE": "str", "PERFECT": "bool"}


# TODO: Handle empty lines
def read_config(config: dict[str, Any], config_file: str):
    try:
        with open(config_file) as cf:
            for line in cf:
                line = line.strip('\n')
                if ' ' in line or '\t' in line:
                    raise ConfigFormatError(line, "Line cannot contain spaces")
                if len(line.split('=')) != 2:
                    raise ConfigFormatError(line, "Line must contain exactly 2 values")
                setting = line.split('=')[0]
                value = line.split('=')[1]
                config[setting] = value
    except ConfigFormatError:
        raise
    except Exception as e:
        print(f"Error reading config file: {e}", file=sys.stderr)
        raise


def parse_config(config: dict[str, Any]):
    if not config.keys() <= SETTINGS_TYPES.keys():
        unknown_settings = config.keys() - SETTINGS_TYPES.keys()
        raise ConfigError(f"Unknown setting(s): '{", ".join(unknown_settings)}'")

    for setting, value in config.items():
        config[setting] = convert_value(setting, value)
    return config


# TODO: Make this more robust and test this
def convert_value(setting: str, value: Any) -> Any:
    match SETTINGS_TYPES[setting]:
        case "int":
            try:
                value = int(value)
            except ValueError:
                raise ConfigError(f"Invalid integer for '{setting}'")
        case "cords":
            if len(value.split(',')) != 2:
                raise ConfigError(f"Invalid cords for '{setting}'")
            try:
                value = (int(value.split(',')[0]), int(value.split(',')[1]))
            except ValueError:
                raise ConfigError(f"Invalid cords for '{setting}'")
        case "bool":
            if value == "True":
                value = True
            elif value == "False":
                value = False
            else:
                raise ConfigError(f"Invalid boolean for '{setting}'")
    return value


# TODO: Value restrictions (f.e. cords < 100, 100)
def validate_config(config: dict[str, Any]):
    if not REQUIRED_SETTINGS <= config.keys():
        missing_settings = REQUIRED_SETTINGS - set(config.keys())
        raise ConfigError(f"Missing setting(s): '{", ".join(missing_settings)}'")


def load_config(config_file: str) -> dict[str, Any]:
    config = {}
    try:
        read_config(config, config_file)
        parse_config(config)
        validate_config(config)
    except ConfigFormatError as e:
        print(f"Invalid config format: {e}", file=sys.stderr)
        raise
    except ConfigError as e:
        print(f"Invalid config: {e}", file=sys.stderr)
        raise
    return config
