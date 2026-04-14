import random


class KruskalMaze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells = width * height
        self.parent = list(range(self.cells))
        self.rank = [0] * self.cells
        self.pathway = []
        self._generate()

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

        return grid

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

    def _generate(self):
        edges = self.generate_edges()
        random.shuffle(edges)
        for edge in edges:
            a, b = self.edge_ids(edge)
            if self.union(a, b):
                self.pathway.append(edge)

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


if __name__ == '__main__':
    maze = KruskalMaze(width=12, height=8)
    print(maze)
    stdgrid = maze.standard_grid()
    for row in stdgrid:
        print(row)
