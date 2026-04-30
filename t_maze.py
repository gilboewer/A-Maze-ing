from dataclasses import dataclass


@dataclass
class Maze:
    """Maze data structure with wall checking logic."""
    width: int = 8
    height: int = 8
    entry: tuple[int, int] = (0, 0)
    exit: tuple[int, int] = (7, 7)
    path: list[tuple[int, int]] = None
    
    def __post_init__(self) -> None:
        """Initialize cells and path."""
        # Hardcoded 8x8 for now - will be replaced by generator
        self.cells = [
            [0xF, 0xB, 0xB, 0x9, 0x3, 0xB, 0xB, 0x7],
            [0xD, 0x6, 0xA, 0x6, 0x9, 0x6, 0xA, 0xD],
            [0xD, 0x5, 0xA, 0x5, 0xE, 0x9, 0x2, 0x5],
            [0xC, 0x5, 0xA, 0x5, 0xB, 0x6, 0x8, 0x5],
            [0x5, 0x7, 0xA, 0x5, 0xE, 0x9, 0x6, 0x9],
            [0xD, 0xD, 0x2, 0x5, 0xB, 0x6, 0x9, 0x6],
            [0xD, 0x5, 0xA, 0x5, 0xE, 0x9, 0x6, 0x9],
            [0x9, 0x5, 0xA, 0x5, 0xA, 0x6, 0xA, 0x6],
        ]
        
        self.path = [
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
            (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)
        ]
    
    def has_wall(self, x: int, y: int, direction: str) -> bool:
        """Check if cell has a wall in given direction.
        
        PORTABLE METHOD - used by both ASCII and MLX renderers.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        cell = self.cells[y][x]
        wall_bits = {'N': 0x1, 'E': 0x2, 'S': 0x4, 'W': 0x8}
        return bool(cell & wall_bits[direction])