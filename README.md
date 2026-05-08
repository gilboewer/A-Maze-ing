*This project has been created as part of the 42 curriculum by gilboewer, kgeromel, spacecodesailor.*

# A-Maze-ing

## Description

A-Maze-ing is an interactive maze generator and visualizer written in Python. The project allows users to generate mazes using Kruskal's algorithm, display them in the terminal with ASCII art, and interact with the maze by toggling the solution path, changing colors, and regenerating new mazes. The goal is to create a fun and educational tool for exploring maze generation algorithms while providing a modular architecture that separates maze generation logic from rendering.

The application features:
- Maze generation using Kruskal's algorithm
- ASCII-based terminal rendering with color support
- Interactive controls for path display, color cycling, and regeneration
- Configurable maze parameters via a text file
- Optional "42" symbol carving in the center of larger mazes

## Instructions

### Installation

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   make install
   ```

### Execution

Run the application with:
```bash
make run
```

- `config_file`: Optional path to a configuration file (defaults to `config.txt` if not provided).

The application will display the maze and show interactive controls. Use the following keys:
- `p`: Toggle path display (show/hide solution)
- `c`: Change wall color (cycles through available colors)
- `r`: Regenerate maze
- `q`: Quit the application

### Configuration File Structure

The configuration file is a plain text file with key-value pairs, one per line. Lines starting with `#` are comments and are ignored. The complete structure is as follows:

```
WIDTH=<int>          # Number of columns (must be > 0)
HEIGHT=<int>         # Number of rows (must be > 0)
ENTRY=<int>,<int>    # Entry coordinates as row,col (must be within bounds)
EXIT=<int>,<int>     # Exit coordinates as row,col (must differ from ENTRY)
OUTPUT_FILE=<str>    # Path to output file for maze data
PERFECT=<bool>       # True for perfect maze (no loops), False for imperfect (adds one loop)
SEED=<int>           # Optional random seed for reproducible mazes
```

Example:
```
WIDTH=11
HEIGHT=11
ENTRY=1,1
EXIT=9,9
OUTPUT_FILE=maze.txt
PERFECT=True
# This is a comment
```

## Maze Generation Algorithm

The project uses **Kruskal's algorithm** for maze generation. Kruskal's algorithm is a minimum spanning tree algorithm that treats maze cells as nodes and possible passages between them as edges. It randomly selects edges and adds them to the maze if they connect different components, ensuring no cycles are formed in perfect mazes.

### Why Kruskal's Algorithm?

Kruskal's algorithm was chosen for several reasons:
- **Efficiency**: It runs in O(E log E) time where E is the number of edges, making it suitable for generating large mazes quickly.
- **Guarantees perfect mazes**: When PERFECT=True, it produces mazes with exactly one path between any two cells.
- **Flexibility**: The algorithm can be easily modified to create imperfect mazes by adding extra passages.
- **Simplicity**: The implementation is straightforward and educational, aligning with the project's learning goals.
- **Union-Find optimization**: Uses path compression and union by rank for optimal performance.

## Reusable Code

The project is designed with modularity in mind, making several components reusable:

### mazegen Package
The `mazegen` package is a standalone library for maze generation that can be imported into other Python projects:
```python
from mazegen import MazeGenerator

config = {...}
generator = MazeGenerator(config)
maze = generator.generate(output_to_file=False)
```

It includes:
- `MazeGenerator` class: Handles configuration and maze creation
- `Maze` class: Represents the generated maze with grid, path, entry, and exit
- Support for perfect and imperfect mazes
- Optional seed for reproducibility

### Renderer System
The rendering system uses inheritance for extensibility:
- `BaseRenderer`: Abstract base class providing common functionality (path toggling, color cycling)
- `ASCIIRenderer`: Concrete implementation for terminal display
- Easy to extend with new renderers (e.g., graphical renderers) by inheriting from `BaseRenderer`

### Utility Modules
- `utils/colours.py`: Color definitions and utilities
- `loadconfig.py`: Configuration file parsing
- `output_validator.py`: Maze validation tools

## Resources

### References
- [Kruskal's Algorithm - Wikipedia](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm): Overview of the algorithm used for maze generation.
- [Maze Generation Algorithm - Jamis Buck](https://weblog.jamisbuck.org/2011/1/3/maze-generation-kruskal-s-algorithm): Detailed explanation of implementing Kruskal's for mazes.
- [Union-Find Data Structure](https://en.wikipedia.org/wiki/Disjoint-set_data_structure): The underlying data structure used in the implementation.
- [Python Documentation](https://docs.python.org/3/): Official Python documentation for language features used.

### AI Usage
AI (GitHub Copilot) was used throughout the development process for:
- Code generation and autocompletion for boilerplate and algorithmic implementations
- Debugging assistance and error resolution
- Documentation writing and README structure suggestions

The core algorithmic logic (Kruskal's implementation) was developed with AI assistance but verified and understood by the developers. AI helped accelerate development while ensuring best practices were followed.</content>
<parameter name="filePath">/home/gil/42-repos/A-Maze-ing/README.md
