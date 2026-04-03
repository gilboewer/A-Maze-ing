from colours import RESET, WALL_COLOURS, ENTRY, EXIT, PATH


def render(maze, show_path, wall_colour):
    print(maze)
    for row in maze.cells:
        for cell in row:
            if cell & 1:  # North wall closed
                print("---")
            else:
                print("   ")


if __name__ == "__main__":
    from stub_maze import Maze
    maze = Maze()
    render(maze, show_path=False, wall_colour=0)
