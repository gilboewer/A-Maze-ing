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
    def __init__(self, height: int, width: int, entry: tuple, exit: tuple):
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.grid: list[list[int]] = []
        self.path: list[tuple] = []


class MazeGenerator:
    def __init__(self, config: dict):
        MazeGenerator.validate(config)
        self.config = config

    def generate(self, output_to_file: bool) -> Maze:
        height, width = self.config["HEIGHT"], self.config["WIDTH"]
        entry, exit = self.config["ENTRY"], self.config["EXIT"]
        perfect = self.config["PERFECT"]

        if "SEED" in self.config:
            random.seed(self.config["SEED"])

        maze = Maze(height, width, entry, exit)
        kmaze = KruskalMaze(height, width, entry, exit, perfect)
        maze.grid = kmaze.standard_grid()
        self.solve_maze(maze)
        if self.output_to_file:
            self.output_to_file(maze)
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
                if maze.grid[r][c] & (1 << wall_bit):
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < maze.height and 0 <= nc < maze.width:
                    neighbor = (nr, nc)
                    if neighbor not in came_from:
                        came_from[neighbor] = current
                        queue.append(neighbor)

    def output_to_file(self, maze: Maze):
        with open(self.config["OUTPUT_FILE"], 'w') as output_file:
            for y in range(maze.height):
                for x in range(maze.width):
                    print(hex(maze.grid[y][x])[2:], end='', file=output_file)
                print(file=output_file)

            print(file=output_file)
            print(f"{maze.entry[1]},{maze.entry[0]}", file=output_file)
            print(f"{maze.exit[1]},{maze.exit[0]}", file=output_file)

            dir_path = self.cell_path_to_dir_path(maze.path)
            for dir in dir_path:
                print(dir, end='', file=output_file)
            print(file=output_file)

    def cell_path_to_dir_path(self, path: list[tuple]) -> list[str]:
        dir_path = []
        for i in range(len(path[:-1])):
            cur = path[i]
            next = path[i + 1]
            cur_y, cur_x = cur
            next_y, next_x = next

            if next_y > cur_y:
                dir_path.append('S')
                continue
            if next_y < cur_y:
                dir_path.append('N')
                continue
            if next_x > cur_x:
                dir_path.append('E')
                continue
            if next_x < cur_x:
                dir_path.append('W')
                continue
        return dir_path

    # TODO: Test with seed
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
                        setting, "Must be a non-zero positive integer")
            elif setting in ("ENTRY", "EXIT"):
                y, x = value
                if x < 0 or y < 0:
                    raise ConfigValueError(
                        setting, "Cannot be negative")
                width, height = config["WIDTH"], config["HEIGHT"]
                if x >= width or y >= height:
                    raise ConfigValueError(
                        setting, "Coordinates exceed maze bounds")
            elif setting == "PERFECT":
                if not isinstance(value, bool):
                    raise ConfigValueError(
                        setting, "Must be valid boolean")

        if config["ENTRY"] == config["EXIT"]:
            raise ConfigError("ENTRY and EXIT must be different coordinates")
