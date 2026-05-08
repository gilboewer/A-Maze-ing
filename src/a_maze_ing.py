"""A-Maze-ing - Maze generator and renderer.

Main entry point for the maze application.
"""
import os
import sys
from renderers import ASCIIRenderer
from loadconfig import load_config
from mazegen import MazeGenerator
from utils import COLOR_NAMES


def clear_screen() -> None:
    """
    Clears the terminal screen.
    """
    os.system('clear' if os.name != 'nt' else 'cls')


def display_menu() -> None:
    """
    Displays the interactive menu options.
    """
    print("\n" + "="*50)
    print("CONTROLS:")
    print("  [p] Toggle path display")
    print("  [c] Change wall color")
    print("  [r] Regenerate maze")
    print("  [q] Quit")
    print("="*50)


def main() -> None:
    """
    Main interactive loop for the maze application.

    Handles user input for toggling path display, changing wall color,
    regenerating maze, and quitting the application.
    """
    if len(sys.argv) > 2:
        raise Exception("Program takes only 1 optional argument: config file")

    # Create maze and renderer
    config = load_config()
    mazegen = MazeGenerator(config)
    maze = mazegen.generate(True)
    renderer = ASCIIRenderer(maze, show_path=False, wall_color="white")

    print("Welcome to A-Maze-ing!")
    print("Loading maze...")

    while True:
        # Clear screen and draw maze
        clear_screen()
        renderer.draw()

        # Show current state
        print(f"\nPath: {'VISIBLE' if renderer.show_path else 'HIDDEN'}")
        print(f"Wall Color: {renderer.wall_color.upper()}")
        if maze.height <= 5 and maze.width <= 7:
            print("Maze is too small for 42 symbol!")

        # Show menu
        display_menu()

        # Get user input
        choice = input("\nYour choice: ").lower().strip()

        if choice == 'p':
            renderer.toggle_path()
            print("Path toggled!")

        elif choice == 'c':
            renderer.cycle_color(COLOR_NAMES)
            print(f"Color changed to: {renderer.wall_color}")

        elif choice == 'r':
            maze = mazegen.generate(True)
            renderer.maze = maze
            print("Maze regenerated!")

        elif choice == 'q':
            print("\nThanks for playing! Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
        print("Exeting program.", file=sys.stderr)
        sys.exit(1)
