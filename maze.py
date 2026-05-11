import numpy as np
import random
from pydantic import (BaseModel, Field, ValidationError, model_validator,
                      PrivateAttr)
from typing_extensions import Self
from collections import deque
import math
from numpy.typing import NDArray


class Configuration(BaseModel):

    """
    Configuration model for maze generation settings.

    Defines the parameters required to generate a maze, including dimensions,
    entry/exit points, output file, and whether the maze is perfect (no loops).

    Attributes:
        width (int): Width of the maze (minimum 2).
        height (int): Height of the maze (minimum 2).
        entry (tuple[int, int]): Coordinates (x, y) of the maze entry point.
        exit (tuple[int, int]): Coordinates (x, y) of the maze exit point.
        output_file (str): File name where the maze will be saved.
        perfect (bool): If True, generates a perfect maze with one solution.
        seed (int): Random seed used for maze generation (default: 42).
        _visited (NDArray[np.int_]): Internal grid tracking visited cells and
            the '42' pattern to avoid placing entry/exit points on it.
    """
    width: int = Field(..., ge=2)
    height: int = Field(..., ge=2)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int = 42
    _visited = PrivateAttr()

    def model_post_init(self, __context) -> None:
        """
        Initialize the _visited grid with the '42' pattern after model
        creation.
        """
        self._visited = self.__write_42()

    def __write_42(self) -> NDArray[np.int_]:
        """
            Return a grid marking the '42' pattern (1 for pattern, 0 otherwise)
        """
        visited = np.full((self.height, self.width), 0)
        if self.height < 8 or self.width < 10:
            return visited
        pattern = [
            '1   111',
            '1     1',
            '111 111',
            '  1 1  ',
            '  1 111'
        ]
        x0 = self.width // 2 - len(pattern[0]) // 2
        y0 = self.height // 2 - len(pattern) // 2
        for y, row in enumerate(pattern):
            for x, value in enumerate(row):
                if value != ' ':
                    visited[y0 + y, x0 + x] = 1
        return visited

    @model_validator(mode='after')
    def check_rules(self) -> Self:
        """
        Validates that the configuration is consistent and valid.

        Ensures that:
        - Entry and exit coordinates are within maze bounds.
        - Entry and exit are not the same point.
        - Entry and exit are not placed in the 42 pattern.

        Returns:
            Self: The validated configuration object.

        Raises:
            ValidationError: If any validation rule is violated.
        """
        if self.entry[0] >= self.width:
            raise ValidationError('The entry x position is higher than the'
                                  'width')
        if self.entry[1] >= self.height:
            raise ValidationError('The entry y position is higher than the'
                                  'height')
        if self.exit[0] >= self.width:
            raise ValidationError('The exit x position is higher than the'
                                  'width')
        if self.exit[1] >= self.height:
            raise ValidationError('The exit y position is higher than the'
                                  'height')
        if self.exit == self.entry:
            raise ValidationError('The exit and the entry must bu different')
        if self._visited[self.entry[1], self.entry[0]] == 1:
            raise ValidationError('The entry position is in the 42 pattern')
        if self._visited[self.exit[1], self.exit[0]] == 1:
            raise ValidationError('The exit position is in the 42 pattern')
        return self


class MazeGenerator():

    _directions = [
                    (0, -1, 0),   # north
                    (1, 0, 1),   # east
                    (0, 1, 2),   # south
                    (-1, 0, 3)  # west
                ]

    def __init__(self, maze_data: Configuration):
        """Initialize the maze generator with configuration data."""
        self.width = maze_data.width
        self.height = maze_data.height
        self.entry = maze_data.entry
        self.exit = maze_data.exit
        self.perfect = maze_data.perfect
        self.maze = np.full((maze_data.height, maze_data.width), 15)
        self.visited = maze_data._visited

    def __get_available_walls(self, col: int, row: int) -> list:
        """Return a list of unvisited neighboring walls for a given cell."""
        walls = []
        for dx, dy, wall in self._directions:
            if (0 <= (col + dx) < self.width and
                    0 <= (row + dy) < self.height and
                    self.visited[row + dy, col + dx] == 0):
                walls.append((col, row, wall))
        return walls

    def __remove_wall(self, neighbor: tuple) -> tuple[int, int]:
        """
            Remove the wall between a cell and its neighbor,
            returning neighbor coordinates.
        """
        col, row, wall = neighbor
        opposite = wall + 2
        if opposite > 3:
            opposite -= 4
        ncol = col + self._directions[wall][0]
        nrow = row + self._directions[wall][1]
        self.maze[row, col] &= ~(1 << wall)
        self.maze[nrow, ncol] &= ~(1 << opposite)
        return (ncol, nrow)

    def __possible_walls(self, position: tuple[int, int]) -> list[int]:
        """
            Return walls that can be safely removed to create 
            loops in the maze.
        """
        col, row = position
        num_position = self.maze[row, col]
        walls: list[int] = []
        if not num_position == 15:
            for num in range(4):
                is_outer_wall = (
                    (num == 0 and row == 0) or
                    (num == 1 and col == self.width - 1) or
                    (num == 2 and row == self.height - 1) or
                    (num == 3 and col == 0)
                )
                if (not is_outer_wall and num_position & (1 << num)):
                    cells_with_walls = True
                    for sum_col in [1, 0, -1]:
                        for sum_row in [1, 0, -1]:
                            ncol = col + sum_col
                            nrow = row + sum_row
                            if (0 <= ncol < self.width and
                               0 <= nrow < self.height):
                                if (self.maze[nrow][ncol] == 0 or
                                   self.maze[nrow][ncol] == 15):
                                    cells_with_walls = False
                                    break
                        if not cells_with_walls:
                            break
                    if cells_with_walls:
                        walls.append(num)
        return walls

    def __more_than_one_solution(self) -> bool:
        """Check if the maze has more than one valid solution."""
        solution = SolutionGenerator(self)
        solution.get_solution()
        return len(solution.solution) > 1

    def __make_no_perfect(self):
        """Randomly remove walls to make the maze imperfect"""
        num_cells = self.width * self.height
        if num_cells < 300:
            num_attemps = math.ceil(0.05 * num_cells)
        elif num_cells < 1000:
            num_attemps = math.ceil(0.1 * num_cells)
        elif num_cells < 3000:
            num_attemps = math.ceil(0.15 * num_cells)
        else:
            num_attemps = math.ceil(0.20 * num_cells)
        attemps = 0
        while attemps < num_attemps:
            position = (random.randint(0, self.width - 1),
                        random.randint(0, self.height - 1))
            walls = self.__possible_walls(position)
            if walls:
                wall = random.choice(walls)
                self.__remove_wall((position[0], position[1], wall))
            attemps += 1

    def gen_maze(self):
        """
            Generate the maze using depth-first search and
            optionally add loops if imperfect.
        """
        self.visited[self.entry[1], self.entry[0]] = 1
        stack = [(self.entry[0], self.entry[1])]
        while stack:
            col, row = stack[-1]
            walls = self.__get_available_walls(col, row)
            if walls:
                wall = random.choice(walls)
                ncol, nrow = self.__remove_wall(wall)
                self.visited[nrow, ncol] = 1
                stack.append((ncol, nrow))
            else:
                stack.pop()
        if not self.perfect:
            self.__make_no_perfect()
            while not self.__more_than_one_solution():
                self.__make_no_perfect()


class SolutionGenerator():

    def __init__(self, maze: MazeGenerator):
        self.maze = maze
        self.solution: list[str] = []

    def get_neighbors(self, col: int, row: int) -> list:
        neighbors = []
        dirs = [
                    (0, -1, 'S'),   # north
                    (1, 0, 'W'),   # east
                    (0, 1, 'N'),   # south
                    (-1, 0, 'E')  # west
        ]
        num_position = self.maze.maze[row, col]
        for num in range(4):
            if not (num_position & (1 << num)):
                x, y, point = dirs[num]
                nx, ny = col + x, row + y
                neighbors.append((nx, ny, point))
        return neighbors

    def get_solution(self):
        queue = deque([[self.maze.entry, [], {self.maze.entry}]])
        while queue:
            position, sol, visited = queue.popleft()
            if position == self.maze.exit:
                self.solution.append("".join(sol))
            else:
                neighbours = self.get_neighbors(position[0], position[1])
                for x, y, point in neighbours:
                    if (x, y) not in visited:
                        new_sol = sol + [point]
                        new_visited = visited | {(x, y)}
                        queue.append([(x, y), new_sol, new_visited])





