class Maze:
    def __init__(self, height: int, width: int, entry: tuple, exit: tuple):
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.grid: list[list[int]] = []
        self.path: list[tuple] = []

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        """Check if cell has a wall in given direction.

        PORTABLE METHOD - used by both ASCII and MLX renderers.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        cell = self.grid[y][x]
        wall_bits = {'N': 0x1, 'E': 0x2, 'S': 0x4, 'W': 0x8}
        return bool(cell & wall_bits[direction])
