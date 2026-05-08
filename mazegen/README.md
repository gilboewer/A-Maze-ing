# mazegen

A Python package for generating mazes using Kruskal's algorithm, with the number **42** carved out in the centre. Mazes can be perfect (a single unique path between any two cells) or imperfect (containing at least one loop).

---

## Installation

Place the `mazegen` package directory in your project and import it directly:

```python
from mazegen import MazeGenerator
```

---

## Quick Start

```python
from mazegen import MazeGenerator

config = {
    "WIDTH":       20,
    "HEIGHT":      15,
    "ENTRY":       (0, 0),      # (row, col) — top-left corner
    "EXIT":        (14, 19),    # (row, col) — bottom-right corner
    "PERFECT":     True,
    "OUTPUT_FILE": "maze.txt",
}

generator = MazeGenerator(config)
maze = generator.generate(output_to_file=False)
```

`generate()` returns a `Maze` object and, when `output_to_file=True`, also writes the maze to `OUTPUT_FILE`.

---

## Configuration Reference

| Key | Type | Required | Description |
|---|---|---|---|
| `WIDTH` | `int` | ✅ | Number of columns. Must be > 0. |
| `HEIGHT` | `int` | ✅ | Number of rows. Must be > 0. |
| `ENTRY` | `tuple[int, int]` | ✅ | Entry cell as `(row, col)`. Must be within bounds. |
| `EXIT` | `tuple[int, int]` | ✅ | Exit cell as `(row, col)`. Must differ from `ENTRY`. |
| `PERFECT` | `bool` | ✅ | `True` for a perfect maze (no loops); `False` adds one extra passage. |
| `OUTPUT_FILE` | `str` | ✅ | Path to the output file (used when `output_to_file=True`). |
| `SEED` | `int` | ❌ | Random seed for reproducible mazes. |

> **Note on the 42 symbol:** The carved-out "42" occupies a 5×7 area in the centre of the grid. It is only rendered when `WIDTH > 7` and `HEIGHT > 5`. Entry and exit coordinates must not fall inside this carved region.

---

## Custom Parameters

### Controlling size

```python
config = {
    "WIDTH":       40,
    "HEIGHT":      30,
    "ENTRY":       (0, 0),
    "EXIT":        (29, 39),
    "PERFECT":     True,
    "OUTPUT_FILE": "big_maze.txt",
}
```

### Reproducible mazes with a seed

```python
config = {
    "WIDTH":       20,
    "HEIGHT":      15,
    "ENTRY":       (0, 0),
    "EXIT":        (14, 19),
    "PERFECT":     True,
    "OUTPUT_FILE": "maze.txt",
    "SEED":        42,           # Same seed → same maze every run
}
```

### Imperfect mazes (with a loop)

Setting `PERFECT` to `False` causes the generator to add one extra passage, creating a loop and giving the maze more than one valid solution.

```python
config = {
    ...
    "PERFECT": False,
    ...
}
```

---

## Accessing the Generated Maze

`MazeGenerator.generate()` returns a `Maze` instance with the following attributes:

| Attribute | Type | Description |
|---|---|---|
| `maze.height` | `int` | Number of rows. |
| `maze.width` | `int` | Number of columns. |
| `maze.entry` | `tuple[int, int]` | Entry cell `(row, col)`. |
| `maze.exit` | `tuple[int, int]` | Exit cell `(row, col)`. |
| `maze.grid` | `list[list[int]]` | 2-D grid of wall-bit integers (see below). |
| `maze.path` | `list[tuple[int, int]]` | Solution path as an ordered list of `(row, col)` cells from entry to exit. |

### The grid

Each cell in `maze.grid` is an integer whose lower four bits encode walls:

| Bit | Direction |
|---|---|
| 0 (`0x1`) | North |
| 1 (`0x2`) | East |
| 2 (`0x4`) | South |
| 3 (`0x8`) | West |

A set bit means a wall is **present** in that direction. You can also use the convenience method `maze.has_wall(x, y, direction)`:

```python
# Check walls around the cell at column 3, row 2
maze.has_wall(3, 2, 'N')  # True if there's a wall to the north
maze.has_wall(3, 2, 'E')  # True if there's a wall to the east
```

### The solution path

`maze.path` is a list of `(row, col)` tuples representing the cells that make up the solution, in order from entry to exit:

```python
maze = generator.generate(output_to_file=False)

print("Solution steps:", len(maze.path))
print("First cell:", maze.path[0])   # same as maze.entry
print("Last cell:",  maze.path[-1])  # same as maze.exit

# Print each step
for row, col in maze.path:
    print(f"  → ({row}, {col})")
```

To get the solution as a sequence of directional moves (`'N'`, `'S'`, `'E'`, `'W'`) rather than coordinates, use the generator's helper:

```python
directions = generator.cell_path_to_dir_path(maze.path)
print("".join(directions))  # e.g. "EESSSWEEN..."
```

---

## Writing to a File

Pass `output_to_file=True` to write the maze to the path specified by `OUTPUT_FILE`:

```python
maze = generator.generate(output_to_file=True)
```

The file format is:

```
<grid rows of hex wall-bit values>

<entry_col>,<entry_row>
<exit_col>,<exit_row>
<direction string, e.g. EESSSWWN...>
```

---

## Error Handling

All errors are subclasses of `ConfigError` and are raised during instantiation (`MazeGenerator(config)`) or generation:

```python
from mazegen import MazeGenerator, ConfigError, ConfigFormatError, ConfigParseError, ConfigValueError

try:
    generator = MazeGenerator(config)
    maze = generator.generate(output_to_file=False)
except ConfigValueError as e:
    print(f"Bad config value: {e}")
except ConfigError as e:
    print(f"Config error: {e}")
```

| Exception | Raised when |
|---|---|
| `ConfigError` | Unknown/missing settings, entry equals exit, or entry/exit inside the 42 symbol. |
| `ConfigValueError` | A setting has a value of the right type but an invalid value (e.g. negative dimensions, out-of-bounds coordinates). |
| `ConfigParseError` | A setting's value could not be parsed into the expected type (raised by config file parsers built on top of this package). |
| `ConfigFormatError` | A config file has a malformed line (raised by config file parsers built on top of this package). |
