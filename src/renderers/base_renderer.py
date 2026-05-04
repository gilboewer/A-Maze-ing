"""Base renderer class with shared logic for all renderers."""
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from t_maze import Maze


@dataclass
class BaseRenderer:
    """Base class for maze renderers.

    Contains portable logic that works for both ASCII and MLX.
    Subclasses only need to implement the drawing primitives.
    """

    maze: 'Maze'
    show_path: bool = False
    wall_color: str = "white"

    def toggle_path(self) -> None:
        """Toggle path visibility."""
        self.show_path = not self.show_path

    def cycle_color(self, color_names: list[str]) -> None:
        """Cycle to next color in the list.

        Args:
            color_names: List of available color names
        """
        try:
            current_index = color_names.index(self.wall_color)
            next_index = (current_index + 1) % len(color_names)
            self.wall_color = color_names[next_index]
        except ValueError:
            # Current color not in list, reset to first
            self.wall_color = color_names[0]

    def is_entry(self, x: int, y: int) -> bool:
        """Check if cell is the entry point."""
        return (y, x) == self.maze.entry

    def is_exit(self, x: int, y: int) -> bool:
        """Check if cell is the exit point."""
        return (y, x) == self.maze.exit

    def is_on_path(self, x: int, y: int) -> bool:
        """Check if cell is on the solution path."""
        return (y, x) in self.maze.path

    def is_on_42(self, x: int, y: int) -> bool:
        return self.maze.grid[y][x] == 0xF

    def draw(self) -> None:
        """Draw the maze. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement draw()")
