# from dataclasses import dataclass, field
import random

from errors import ConfigError, ConfigValueError
from kruskal import KruskalMaze


# @dataclass
# class Maze:
#     width: int
#     height: int
#     entry: tuple[int, int]
#     exit: tuple[int, int]
#     grid: list[list[int]] = field(default_factory=list)
#     path: list[tuple[int, int]] = field(default_factory=list)


class Maze:
    def __init__(self, width: int, height: int, entry: tuple, exit: tuple):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: list[list[int]] = []
        self.path: list[tuple] = []


class MazeGenerator:
    def __init__(self, config: dict):
        MazeGenerator.validate(config)
        self.config = config

    def generate(self) -> Maze:
        width, height = self.config["HEIGHT"], self.config["WIDTH"]
        entry, exit = self.config["ENTRY"], self.config["EXIT"]
        perfect = self.config["PERFECT"]

        if "SEED" in self.config:
            random.seed(self.config["SEED"])

        maze = Maze(width, height, entry, exit)
        maze.grid = KruskalMaze(width, height, perfect).standard_grid()
        self.solve_maze(maze)
        return maze

    def solve_maze(self, maze: Maze) -> None:
        NORTH = 0
        EAST = 1
        SOUTH = 2
        WEST = 3

        DIRECTIONS = [
            (-1,  0, NORTH, SOUTH),
            (0, +1, EAST,  WEST),
            (+1,  0, SOUTH, NORTH),
            (0, -1, WEST,  EAST),
        ]

        start, end = maze.entry, maze.exit
        queue = [start]
        came_from: dict = {start: None}

        while queue:
            current = queue.pop(0)
            if current == end:
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                maze.path = path[::-1]
                return

            r, c = current
            for dr, dc, wall_bit, _ in DIRECTIONS:
                # Move is allowed when the wall bit is 0 (passage present)
                if maze.grid[r][c] & (1 << wall_bit):
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < maze.height and 0 <= nc < maze.width:
                    neighbor = (nr, nc)
                    if neighbor not in came_from:
                        came_from[neighbor] = current
                        queue.append(neighbor)

    # TODO: Test entry and exit different coords exception
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
            elif setting in ("ENTRY", "EXIT"):
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

        if config["ENTRY"] == config["EXIT"]:
            raise ConfigError("ENTRY and EXIT must be different coordinates")
