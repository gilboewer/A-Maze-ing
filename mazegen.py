from errors import ConfigError, ConfigValueError


class Maze:
    def __init__(self, width, height, entry, exit):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.path = []
        self.grid = [[0 for _ in range(width)] for _ in range(height)]


class MazeGenerator:
    def __init__(self, config: dict):
        self.config = config

    # TODO: Add optional settings
    # TODO: Test
    @staticmethod
    def validate_config(config):
        REQUIRED_SETTINGS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}  # noqa: E501
        OPTIONAL_SETTINGS = {"SEED"}  # noqa: E501

        if not config.keys() <= OPTIONAL_SETTINGS:
            unknown_settings = config.keys() - OPTIONAL_SETTINGS
            raise ConfigError(
                f"Unknown setting(s): '{", ".join(unknown_settings)}'")

        if not REQUIRED_SETTINGS <= config.keys():
            missing_settings = REQUIRED_SETTINGS - set(config.keys())
            raise ConfigError(
                f"Missing setting(s): '{", ".join(missing_settings)}'")

        for setting, value in config.items():
            if setting in ("WIDTH", "HEIGHT"):
                if value <= 0:
                    raise ConfigValueError(
                        setting, value, "Must be a non-zero positive integer")
            elif setting in ("Entry", "EXIT"):
                x, y = value
                if x < 0 or y < 0:
                    raise ConfigValueError(
                        setting, value, "Cannot be negative")
                width, height = config["WIDTH"], config["HEIGHT"]
                if x >= width or y >= height:
                    raise ConfigValueError(
                        setting, value,
                        "Coordinates exceed maze bounds"
                        f" ({width - 1}, {height - 1})")
            elif setting == "PERFECT":
                if not isinstance(value, bool):
                    raise ConfigValueError(
                        setting, value, "Must be valid boolean")
