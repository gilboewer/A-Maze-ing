from dataclasses import dataclass


@dataclass
class Maze:
    """Hardcoded 5x5 maze for renderer development."""

    width: int = 5
    height: int = 5
    entry: tuple[int, int] = (0, 0)
    exit: tuple[int, int] = (4, 4)
    path: list[tuple[int, int]] = None

    def __post_init__(self) -> None:
        """Initialize cells and path."""
        # Each cell: 4-bit int, bits = N E S W (LSB = North)
        # 1=N 2=E 4=S 8=W
        self.cells = [
            [0xF, 0xB, 0xB, 0xB, 0x7],
            [0xD, 0x6, 0x9, 0x6, 0xD],
            [0xD, 0x5, 0xE, 0x9, 0x5],
            [0xD, 0x6, 0xB, 0x6, 0x9],
            [0x9, 0xA, 0xA, 0xA, 0x6],
        ]
        self.path = [
            (0, 0), (0, 1), (0, 2), (0, 3),
            (1, 3), (2, 3), (2, 4), (3, 4), (4, 4)
        ]
