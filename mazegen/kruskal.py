import random
import sys

from errors import ConfigError


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
        self.pathway = []
        self._generate()
        print(self)

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

    def carve_42symbol(self, grid: list[list[bool]]):
        if self.height > 5 and self.width > 7:
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
        else:
            print("Maze too small, omitting 42 symbol.", file=sys.stderr)

    def carve_line(self, s: tuple, hor: bool,
                   len: int, grid: list[list[bool]]):
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

    # TODO: Remove print
    def _generate(self):
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

    def __str__(self):
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

    def _corner(self, down_left, down_right, right_up, right_down):
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
