class Maze:
    """
    Represents a maze with grid, entry, exit, and path.
    """

    def __init__(self, height: int, width: int, entry: tuple, exit: tuple):
        """
        Initializes the Maze.

        Args:
            height (int): Maze height.
            width (int): Maze width.
            entry (tuple): Entry coordinates (y, x).
            exit (tuple): Exit coordinates (y, x).
        """
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.grid: list[list[int]] = []
        self.path: list[tuple] = []

    def has_wall(self, x: int, y: int, direction: str) -> bool:
        """
        Checks if the cell has a wall in the given direction.

        Portable method used by both ASCII and MLX renderers.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
            direction (str): Direction ('N', 'E', 'S', 'W').

        Returns:
            bool: True if wall exists, False otherwise.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        cell = self.grid[y][x]
        wall_bits = {'N': 0x1, 'E': 0x2, 'S': 0x4, 'W': 0x8}
        return bool(cell & wall_bits[direction])
