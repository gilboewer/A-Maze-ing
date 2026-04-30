"""A-Maze-ing - Maze generator and renderer.

Main entry point for the maze application.
"""
import os
from t_maze import Maze
from renderers import ASCIIRenderer


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def display_menu() -> None:
    """Display the interactive menu options."""
    print("\n" + "="*50)
    print("CONTROLS:")
    print("  [p] Toggle path display")
    print("  [c] Change wall color")
    print("  [r] Regenerate maze")
    print("  [q] Quit")
    print("="*50)


def main() -> None:
    """Main interactive loop."""
    # Create maze and renderer
    maze = Maze()
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
        
        # Show menu
        display_menu()
        
        # Get user input
        choice = input("\nYour choice: ").lower().strip()
        
        if choice == 'p':
            renderer.toggle_path()
            print("Path toggled!")
        
        elif choice == 'c':
            renderer.cycle_color()
            print(f"Color changed to: {renderer.wall_color}")
        
        elif choice == 'r':
            # For now, just create a new Maze instance
            # Later this will call your MazeGenerator
            maze = Maze()
            renderer.maze = maze
            print("Maze regenerated!")
        
        elif choice == 'q':
            print("\nThanks for playing! Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()