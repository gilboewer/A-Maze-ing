# A-Maze-ing

*This project has been created as part of the 42 curriculum by [gboewer] & [kgeromel].*

---

## Description

A-Maze-ing is a maze generator and visualization tool written in Python. The project generates random mazes with configurable parameters and provides an interactive ASCII terminal interface for visualization. The maze generation logic is designed to be reusable and can be integrated into other projects as a standalone package.

**Current Status:** Chapter V (Visual Representation) - WIP

The project currently features:
- ASCII terminal-based maze rendering with colored walls
- Interactive controls for path visualization
- Entry and exit markers
- Scalable rendering (works with any maze size)
- Modular architecture ready for MLX graphical rendering
- Missing 42 logo

---

## Features

### Visual Representation (Chapter V - Complete)
- ✅ **ASCII Terminal Rendering** - Clean text-based maze display
- ✅ **Entry/Exit Markers** - Clear indication of start (E) and end (X) points
- ✅ **Interactive Controls**:
  - Toggle path visibility (show/hide solution)
  - Cycle through wall colors (white, red, green, blue, yellow, magenta, cyan)
  - Regenerate maze (currently reloads hardcoded maze)
  - Quit application
- ✅ **Scalable Design** - Renderer works with any maze dimensions

### In Development
- ⏳ "42" pattern visualization
- ⏳ MLX graphical rendering

---

## Project Structure / Renderer Only - Without generated maze

```
a-maze-ing/
├── a_maze_ing.py              # Main entry point with interactive loop
├── maze.py                    # Maze data structure and wall checking logic
├── renderers/
│   ├── __init__.py           # Package initialization
│   ├── base_renderer.py      # Base renderer class (portable logic)
│   └── ascii_renderer.py     # ASCII terminal renderer implementation
├── utils/
│   ├── __init__.py           # Package initialization
│   └── colours.py            # ANSI color codes and colorization utilities
├── config.txt                # Default configuration file (TODO)
├── README.md                 # This file
└── Makefile                  # Build automation (TODO)
```

---

## Instructions

### Requirements
- Python 3.10 or later
- Terminal with ANSI color support

### Installation

1. Clone the repository:
```bash
git clone <repository_url>
cd a-maze-ing
```

2. No external dependencies required for basic ASCII rendering

### Running the Application

```bash
python3 a_maze_ing.py
```

### Interactive Controls

Once the maze is displayed, you can use the following commands:

| Key | Action |
|-----|--------|
| `p` | Toggle path display (show/hide solution) |
| `c` | Change wall color (cycles through available colors) |
| `r` | Regenerate maze (reload maze - will connect to generator later) |
| `q` | Quit the application |

---

## Architecture Overview

### Portable Design Philosophy

The codebase is architected with **portability** in mind, separating rendering logic from maze logic:

**Portable Components** (Shared between ASCII and MLX):
- `Maze` class - Data structure and wall checking
- `BaseRenderer` - Common logic (path toggling, color cycling, entry/exit checking)
- Maze generation algorithms (when implemented)

**Renderer-Specific Components**:
- `ASCIIRenderer` - Terminal-based drawing using print statements
- `MLXRenderer` (future) - Graphical rendering using pixel buffers

This separation allows approximately **60-70% code reuse** when transitioning from ASCII to graphical rendering.

### Maze Data Structure

Mazes are represented using a **hexadecimal wall encoding**:
- Each cell stores a 4-bit value (0x0 to 0xF)
- Each bit represents a wall direction:
  - Bit 0 (value 1): North wall
  - Bit 1 (value 2): East wall
  - Bit 2 (value 4): South wall
  - Bit 3 (value 8): West wall

**Example:** `0xF = 1111 binary` = all 4 walls present

### Code Reusability

**Reusable Module:** `t_maze.py`

The `Maze` class provides:
- `has_wall(x, y, direction)` - Check if a cell has a wall in a given direction
- Wall data access through clean API
- Entry/exit coordinate storage
- Solution path storage

**Usage Example:**
```python
from maze import Maze

# Create a maze instance
maze = Maze(width=10, height=10)

# Check for walls
if maze.has_wall(0, 0, 'N'):
    print("North wall exists at (0,0)")

# Access maze properties
print(f"Entry: {maze.entry}")
print(f"Exit: {maze.exit}")
```

This module will be packaged as `mazegen-*.whl` for easy installation via pip (Chapter VI).

---

## Team and Project Management

### Team Members
- [gboewer] & [kgeromel]

### Roles
- **Architecture & Design** - Designed modular structure for ASCII/MLX portability
- **ASCII Renderer Implementation** - Built terminal visualization system
- **Interactive Controls** - Implemented user input handling
- **Documentation** - Created comprehensive code documentation and README

### Tools Used
- **Python 3.10+** - Primary development language
- **Git** - Version control
- **VSCode** - Code editor
- **Terminal** - Testing and visualization
- **AI Assistant (Claude)** - Code review, architecture discussions, documentation assistance

---

## AI Usage

### How AI Was Used

AI tools were used to assist with the following aspects of the project:

1. **Architecture Design**
   - Discussed portable design patterns for renderer separation
   - Reviewed modular structure for ASCII/MLX compatibility

2. **Code Development**
   - Helped design the interactive menu system

3. **Documentation**
   - Created comprehensive inline documentation
   - Generated this README structure
   - Explained technical concepts in comments

### What AI Did NOT Do

- **Algorithmic Decisions** - All architectural choices were human-driven
- **Testing** - All code was manually tested and validated
- **Problem-Solving** - Core logic and debugging were done independently
- **Understanding** - Every line of code is fully understood and can be explained

### Critical Review

All AI-generated content was:
- ✅ Reviewed line-by-line for correctness
- ✅ Tested in the actual runtime environment
- ✅ Modified to fit project-specific requirements
- ✅ Validated against project specifications

---

## License

This project is part of the 42 school curriculum and is for educational purposes.

---

*Last Updated: [30/04/2026]*
*Status: Chapter V WIP - ASCII Renderer Functional*