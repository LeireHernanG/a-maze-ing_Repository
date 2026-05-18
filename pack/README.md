# mazegen

A reusable Python package for maze generation and solving.

---

## Installation

Build and install the package:

```bash
python -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

You can also install the source archive:

```bash
pip install dist/mazegen-1.0.0.tar.gz
```

---

## Basic Usage

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
		width=5,
		height=5,
		entry=(0, 0),
		exit=(3, 3),
		perfect=False
)

maze.gen_maze()

print(maze.structure())
```

---

## Custom Parameters

The generator accepts custom parameters such as seed.

Example:

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
		width=5,
		height=5,
		entry=(0, 0),
		exit=(3, 3),
		perfect=False,
		seed=123
)

maze.generate()
```

### Parameters

* `width` (`int`) :
  Width of the maze.

* `height` (`int`) :
  Height of the maze.

* `entry` (`tuple[int, int]`) :
  Entry point coordinates (x, y).

* `exit` (`tuple[int, int]`) :
  Exit point coordinates (x, y).

* `perfect` (`bool`) :
  If True, generates a perfect maze (one solution).

* `seed` (`int`, optional) :
  Random seed used to generate reproducible mazes.

---

## Accessing the Maze Structure

The generated maze structure can be accessed directly from the generator.

Example:

```python
structure = maze.structure

print(structure)
```
---

## Accessing a Maze Solution

The module also provides all valid solution paths in asscending order of length.

Example:

```python
solution = maze.solutions

# All solutions
print(solution)

# Shortest solution
print(solution[0])
```

The solution is returned as a sequence of coordinates representing a valid path from the maze entrance to the exit.

---

## Example

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
		width=5,
		height=5,
		entry=(0, 0),
		exit=(3, 3),
		perfect=False,
		seed=123
)

maze.gen_maze()

print("Maze structure:")
print(maze.structure)

print("Maze solution:")
print(maze.solution[0])
```

---

## Package Structure

```text
mazegen/
├── __init__.py
└── generator.py
```

Main class:

* `MazeGenerator`

---

## Build Instructions

To rebuild the package from source:

```bash
python -m pip install --upgrade build
python -m build
```

Generated files will be available inside the `dist/` directory.

Example:

```text
dist/
├── mazegen-1.0.0.tar.gz
└── mazegen-1.0.0-py3-none-any.whl
```
