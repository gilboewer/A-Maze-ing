"""ASCII terminal renderer for mazes."""
from dataclasses import dataclass
from typing import TYPE_CHECKING
from ..renderers import BaseRenderer
from ..utils import colorize

if TYPE_CHECKING:
    from t_maze import Maze


@dataclass
class ASCIIRenderer(BaseRenderer):
    """
    Renders a maze using ASCII characters in the terminal.
    """

    maze: 'Maze'
    show_path: bool = False
    wall_color: str = "white"

    def draw(self) -> None:
        """
        Draws the entire maze with colors and markers.
        """
        for y in range(self.maze.height):
            self._draw_top_edge(y)
            self._draw_cell_interior(y)
        self._draw_bottom_edge()

    def _draw_top_edge(self, y: int) -> None:
        """
        Draws the top horizontal edges for row y.

        Args:
            y (int): Row index.
        """
        line = ""
        for x in range(self.maze.width):
            line += colorize("+", self.wall_color)
            if y == 0:
                line += colorize("---", self.wall_color)
            elif self.maze.has_wall(x, y, 'N'):
                line += colorize("---", self.wall_color)
            else:
                line += "   "
        line += colorize("+", self.wall_color)
        print(line)

    def _draw_cell_interior(self, y: int) -> None:
        """
        Draws the cell interiors for row y.

        Args:
            y (int): Row index.
        """
        line = ""
        for x in range(self.maze.width):
            # Draw left wall or boundary
            if x == 0:
                line += colorize("|", self.wall_color)
            elif self.maze.has_wall(x, y, 'W'):
                line += colorize("|", self.wall_color)
            else:
                line += " "

            # Draw cell content
            content = self._get_cell_content(x, y)
            line += content

        # Draw right boundary
        line += colorize("|", self.wall_color)
        print(line)

    def _draw_bottom_edge(self) -> None:
        """
        Draws the bottom boundary of the maze.
        """
        line = ""
        for x in range(self.maze.width):
            line += colorize("+", self.wall_color)
            line += colorize("---", self.wall_color)
        line += colorize("+", self.wall_color)
        print(line)

    def _get_cell_content(self, x: int, y: int) -> str:
        """
        Gets the content to display in a cell.

        Priority:
        1. Entry marker (E)
        2. Exit marker (X)
        3. Path marker (•) if show_path is True
        4. Empty space

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.

        Returns:
            str: Cell content string.
        """
        if self.is_entry(x, y):
            return " E "

        if self.is_exit(x, y):
            return " X "

        if self.show_path and self.is_on_path(x, y):
            return " • "

        if self.is_on_42(x, y):
            return " # "

        return "   "

    def cycle_color(self, color_names: list[str]) -> None:
        """
        Cycles to the next wall color.

        Args:
            color_names (list[str]): List of available color names.
        """
        super().cycle_color(color_names)
