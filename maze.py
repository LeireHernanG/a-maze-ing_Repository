import numpy as np
import random
from collections import deque
import math


class MazeGenerator:
    """
    MazeGenerator: Generates a maze using depth-first search
    with optional loops.

    Attributes:
        width (int): Width of the maze (minimum 2).
        height (int): Height of the maze (minimum 2).
        entry (tuple[int, int]): Entry point coordinates (x, y).
        exit (tuple[int, int]): Exit point coordinates (x, y).
        perfect (bool): If True, generates a perfect maze (one solution).
        seed (int): Random seed for reproducibility (default=42).
        output_file (str): Optional file name for saving the maze
        (not used in generation).
        maze (np.ndarray): Generated maze represented as integers
        (bitwise walls).
        solution (list[str]): List of solution paths from entry to exit.

    Example:
        generator = maze = MazeGenerator(
                                width=5,
                                height=5,
                                entry=(0, 0),
                                exit=(3, 3),
                                output_file=maze.txt,
                                perfect=False,
                                seed=123
        )
        generator.gen_maze()
        print(generator.maze)        # Access maze structure
        print(generator.solution)    # Access solution(s)
    """

    _directions = [
                    (0, -1, 0),   # north
                    (1, 0, 1),   # east
                    (0, 1, 2),   # south
                    (-1, 0, 3)  # west
                ]

    def __init__(
                    self, width: int, height: int, entry: tuple[int, int],
                    exit: tuple[int, int], output_file: str, perfect: bool,
                    seed: int = 42
                ):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.output_file = output_file
        self.maze = np.full((height, width), 15)
        self._visited = np.full((height, width), 0)
        self.solution: list[str] = []
        self.__write_42()
        self.__validate()

    def __validate(self) -> None:
        """Validate maze parameters and entry/exit positions."""
        if self.width < 2:
            raise ValueError('The width must be higher')
        if self.height < 2:
            raise ValueError('The height must be higher')
        if not (0 <= self.entry[0] < self.width - 1):
            raise ValueError('The entry x position is out of bounds')
        if not (0 <= self.entry[1] < self.height - 1):
            raise ValueError('The entry y position is out of bounds')
        if not (0 <= self.exit[0] < self.width - 1):
            raise ValueError('The exit x position is out of bounds')
        if not (0 <= self.exit[1] < self.height):
            raise ValueError('The exit y position is out of bounds')
        if self.exit == self.entry:
            raise ValueError('The exit and the entry must bu different')
        if self._visited[self.entry[1], self.entry[0]] == 1:
            raise ValueError('The entry position is in the 42 pattern')
        if self._visited[self.exit[1], self.exit[0]] == 1:
            raise ValueError('The exit position is in the 42 pattern')

    def __write_42(self) -> None:
        """
            Mark the '42' pattern in the visited grid to block entry/exit
            placement and open walls in this cellls.
        """
        if self.height < 8 or self.width < 10:
            return
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
                    self._visited[y0 + y, x0 + x] = 1

    def __accessible_neighbors(
        self, col: int, row: int
    ) -> list[tuple[int, int, str]]:
        """Return accessible neighbors of a cell for computing solutions."""
        neighbors = []
        points = ['N', 'E', 'S', 'W']
        cell_value = self.maze[row, col]
        for num in range(4):
            if not (cell_value & (1 << num)):
                x, y, direction = self._directions[num]
                nx, ny = col + x, row + y
                neighbors.append((nx, ny, points[direction]))
        return neighbors

    def __compute_solution(self) -> None:
        """Compute all possible solutions from entry to exit."""
        self.solution.clear()
        queue: deque[
            tuple[
                tuple[int, int],
                list[str],
                set[tuple[int, int]]
            ]
        ] = deque()
        queue.append((self.entry, [], {self.entry}))
        while queue:
            position, sol, visited = queue.popleft()
            if position == self.exit:
                self.solution.append("".join(sol))
            else:
                neighbours = self.__accessible_neighbors(
                    position[0],
                    position[1]
                )
                for x, y, point in neighbours:
                    if (x, y) not in visited:
                        new_sol = sol + [point]
                        new_visited = visited | {(x, y)}
                        queue.append(((x, y), new_sol, new_visited))

    def __get_available_walls(
            self, col: int, row: int
    ) -> list[tuple[int, int, int]]:
        """Return unvisited neighboring walls for DFS generation."""
        walls = []
        for dx, dy, wall in self._directions:
            if (0 <= (col + dx) < self.width and
                    0 <= (row + dy) < self.height and
                    self._visited[row + dy, col + dx] == 0):
                walls.append((col, row, wall))
        return walls

    def __remove_wall(self, neighbor: tuple[int, int, int]) -> tuple[int, int]:
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
        """Return walls that can be removed to create loops."""
        col, row = position
        cell_value = self.maze[row, col]
        walls: list[int] = []
        if not cell_value == 15:
            for num in range(4):
                is_outer_wall = (
                    (num == 0 and row == 0) or
                    (num == 1 and col == self.width - 1) or
                    (num == 2 and row == self.height - 1) or
                    (num == 3 and col == 0)
                )
                if (not is_outer_wall and cell_value & (1 << num)):
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

    def __make_no_perfect(self) -> None:
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

    def gen_maze(self) -> None:
        """
            Generate the maze using depth-first search and
            optionally add loops if imperfect.
        """
        self._visited[self.entry[1], self.entry[0]] = 1
        stack = [(self.entry[0], self.entry[1])]
        while stack:
            col, row = stack[-1]
            walls = self.__get_available_walls(col, row)
            if walls:
                wall = random.choice(walls)
                ncol, nrow = self.__remove_wall(wall)
                self._visited[nrow, ncol] = 1
                stack.append((ncol, nrow))
            else:
                stack.pop()
        self.__compute_solution()
        if not self.perfect:
            self.__make_no_perfect()
            self.__compute_solution()
            while len(self.solution) <= 1:
                self.__make_no_perfect()
                self.__compute_solution()
