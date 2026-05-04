# from dataclasses import dataclass, field
import random

from errors import ConfigError, ConfigValueError
from t_maze import Maze


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
        if output_to_file:
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

    def output_to_file(self, maze: Maze) -> None:
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
    def validate(config: dict) -> None:
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


# TODO: Remove __str__ (although maybe its ok, keep in for debugging)
class KruskalMaze:
    def __init__(self, height: int, width: int,
                 entry: tuple, exit: tuple, perfect: int = True):
        self.height = height
        self.width = width
        self.perfect = perfect
        self.entry = entry
        self.exit = exit
        self.cells = width * height
        self.parent = list(range(self.cells))
        self.rank = [0] * self.cells
        self.pathway: list[tuple] = []
        self._generate()
        # print(self)

    def root(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.root(a), self.root(b)
        if ra == rb:
            return False

        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True

    def cell_id(self, row: int, col: int) -> int:
        return row * self.width + col

    def generate_grid(self) -> list[list[bool]]:
        grid = [
            [True for _ in range(self.width)]
            for _ in range(self.height)
        ]

        self.carve_42symbol(grid)

        entry_y, entry_x = self.entry
        exit_y, exit_x = self.exit
        if grid[entry_y][entry_x] is False:
            raise ConfigError("Entry coords are inside 42 symbol")
        if grid[exit_y][exit_x] is False:
            raise ConfigError("Exit coords are inside 42 symbol")
        return grid

    def carve_42symbol(self, grid: list[list[bool]]) -> None:
        if self.height <= 5 and self.width <= 7:
            return

        hor = True
        ver = False
        vstart_42 = (self.height - 5) // 2
        hstart_42 = (self.width - 7) // 2

        # 4
        self.carve_line((vstart_42, hstart_42), ver, 3, grid)
        self.carve_line((vstart_42 + 2, hstart_42), hor, 3, grid)
        self.carve_line((vstart_42 + 2, hstart_42 + 2), ver, 3, grid)

        # 2
        self.carve_line((vstart_42, hstart_42 + 4), hor, 3, grid)
        self.carve_line((vstart_42, hstart_42 + 6), ver, 3, grid)
        self.carve_line((vstart_42 + 2, hstart_42 + 4), hor, 3, grid)
        self.carve_line((vstart_42 + 2, hstart_42 + 4), ver, 3, grid)
        self.carve_line((vstart_42 + 4, hstart_42 + 4), hor, 3, grid)

    def carve_line(self, s: tuple, hor: bool,
                   len: int, grid: list[list[bool]]) -> None:
        y, x = s
        if hor:
            for i in range(len):
                grid[y][x + i] = False
        else:
            for i in range(len):
                grid[y + i][x] = False

    def generate_edges(self) -> list[tuple]:
        grid = self.generate_grid()
        edges = []
        for r in range(self.height):
            for c in range(self.width):
                if not grid[r][c]:
                    continue
                if c + 1 < self.width and grid[r][c + 1] is True:
                    edges.append((r, c, 'right'))
                if r + 1 < self.height and grid[r + 1][c] is True:
                    edges.append((r, c, 'down'))
        return edges

    def edge_ids(self, edge: tuple) -> tuple:
        r, c, direction = edge
        if direction == 'right':
            neighbor = (r, c + 1)
        else:
            neighbor = (r + 1, c)

        a = self.cell_id(r, c)
        b = self.cell_id(*neighbor)

        return (a, b)

    def _generate(self) -> None:
        edges = self.generate_edges()
        random.shuffle(edges)
        rejected = []
        for edge in edges:
            a, b = self.edge_ids(edge)
            if self.union(a, b):
                self.pathway.append(edge)
            else:
                rejected.append(edge)

        if not self.perfect:
            self.pathway.append(rejected[0])

    def standard_grid(self) -> list[list[int]]:
        grid = [[0b1111 for _ in range(self.width)]
                for _ in range(self.height)]

        for r, c, direction in self.pathway:
            if direction == 'right':
                grid[r][c] &= ~(1 << 1)
                grid[r][c + 1] &= ~(1 << 3)
            elif direction == 'down':
                grid[r][c] &= ~(1 << 2)
                grid[r + 1][c] &= ~(1 << 0)
        return grid

    def __str__(self) -> str:
        open_right = {(r, c) for r, c, d in self.pathway if d == 'right'}
        open_down = {(r, c) for r, c, d in self.pathway if d == 'down'}

        lines = []
        lines.append('┌' + ('───┬' * (self.width - 1)) + '───┐')

        for r in range(self.height):
            row = '│'
            for c in range(self.width):
                row += '   '
                row += ' ' if (r, c) in open_right else '│'
            lines.append(row)

            if r < self.height - 1:
                wall = '├' if True else ''
                wall = ''
                for c in range(self.width):
                    wall += '   ' if (r, c) in open_down else '───'
                    if c < self.width - 1:
                        down_left = (r, c) not in open_down
                        down_right = (r, c + 1) not in open_down
                        right_up = (r, c) not in open_right
                        right_down = (r + 1, c) not in open_right
                        wall += self._corner(down_left, down_right,
                                             right_up, right_down)
                    else:
                        wall += ('┤' if (r, c) not in open_down
                                 else '╢' if False else '│')
                lines.append('├' + wall + '┤')

        lines.append('└' + ('───┴' * (self.width - 1)) + '───┘')
        return '\n'.join(lines)

    def _corner(self, down_left: bool, down_right: bool,
                right_up: bool, right_down: bool) -> str:
        table = {
            (True,  True,  True,  True): '┼',
            (True,  True,  False, False): '─',
            (False, False, True,  True): '│',
            (True,  False, True,  False): '┘',
            (True,  False, False, True): '└',
            (False, True,  True,  False): '┐',
            (False, True,  False, True): '┌',
            (True,  True,  True,  False): '┴',
            (True,  True,  False, True): '┴',
            (True,  False, True,  True): '┤',
            (False, True,  True,  True): '├',
            (True,  True,  True,  True): '┼',
        }
        return table.get((down_left, down_right, right_up, right_down), '┼')
