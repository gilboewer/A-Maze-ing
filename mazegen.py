from dataclasses import dataclass, field
import random

from errors import ConfigError, ConfigValueError
from kruskal import KruskalMaze


@dataclass
class Maze:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    grid: list[list[int]] = field(default_factory=list)
    path: list[tuple[int, int]] = field(default_factory=list)


# class Maze:
#     def __init__(self, width: int, height: int):
#         self.width = width
#         self.height = height
#         self.entry = entry
#         self.exit = exit
#         self.grid = [[0b1111 for _ in range(width)] for _ in range(height)]
#         self.path = []


class MazeGenerator:
    def __init__(self, config: dict):
        MazeGenerator.validate(config)
        self.config = config

    def generate(self) -> Maze:
        width, height = self.config["HEIGHT"], self.config["WIDTH"]

        if "SEED" in self.config:
            random.seed(self.config["SEED"])

        grid = KruskalMaze(width, height).standard_grid()

    # TODO: Add optional settings
    @staticmethod
    def validate(config: dict):
        REQUIRED_SETTINGS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}  # noqa: E501
        OPTIONAL_SETTINGS = {"SEED"}  # noqa: E501
        SETTINGS = REQUIRED_SETTINGS | OPTIONAL_SETTINGS

        if not config.keys() <= SETTINGS:
            unknown_settings = config.keys() - SETTINGS
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
