import numpy as np
import random
from pydantic import (BaseModel, Field, ValidationError, model_validator, PrivateAttr)
from typing import Any
from typing_extensions import Self
from collections import deque
import math
from numpy.typing import NDArray


# north = 3
# east = 2
# south = 1
# west = 0

class Configuration(BaseModel):
    """
    Configuration model for maze generation settings.

    This class defines the parameters required to generate a maze,
    including its dimensions, entry and exit points, output file,
    and whether the maze must be perfect (without loops).

    Attributes:
        width (int): Width of the maze (must be >= 2).
        height (int): Height of the maze (must be >= 2).
        entry (tuple[int, int]): Coordinates (x, y) of the maze entry point.
        exit (tuple[int, int]): Coordinates (x, y) of the maze exit point.
        output_file (str): File name where the maze will be saved.
        perfect (bool): If True, generates a perfect maze (no cycles).
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
        self._visited = self.write_42()

    def write_42(self) -> NDArray[np.int_]:
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

        Returns:
            Self: The validated configuration object.

        Raises:
            ValueError: If any validation rule is violated.
        """
        if self.entry[0] >= self.width:
            raise ValueError('The entry x position is higher than the width')
        if self.entry[1] >= self.height:
            raise ValueError('The entry y position is higher than the height')
        if self.exit[0] >= self.width:
            raise ValueError('The exit x position is higher than the width')
        if self.exit[1] >= self.height:
            raise ValueError('The exit y position is higher than the height')
        if self.exit == self.entry:
            raise ValueError('The exit and the entry must bu different')
        if self._visited[self.entry[1], self.entry[0]]:
            raise ValueError('The entry position is in the 42 pattern')
        if self._visited[self.exit[1], self.exit[0]]:
            raise ValueError('The exit position is in the 42 pattern')
        return self


class MazeGenerator():

    _directions = [
                    (0, -1, 0),   # north
                    (1, 0, 1),   # east
                    (0, 1, 2),   # south
                    (-1, 0, 3)  # west           
                ]

    def __init__(self, maze_data: Configuration):
        self.width = maze_data.width
        self.height = maze_data.height
        self.entry = maze_data.entry
        self.exit = maze_data.exit
        self.perfect = maze_data.perfect
        self.maze = np.full((maze_data.height, maze_data.width), 15)
        self.visited = maze_data._visited

    def get_available_walls(self, col: int, row: int) -> list:
        walls = []
        for dx, dy, wall in self._directions:
            if (0 <= (col + dx) < self.width and
                    0 <= (row + dy) < self.height and
                    self.visited[row + dy, col + dx] == 0):
                walls.append((col, row, wall))
        return walls

    def remove_wall(self, neighbor: tuple) -> tuple[int, int]:
        col, row, wall = neighbor 
        opposite = wall + 2
        if opposite > 3:
            opposite -= 4
        ncol = col + self._directions[wall][0]
        nrow = row + self._directions[wall][1]
        self.maze[row, col] &= ~(1 << wall)
        self.maze[nrow, ncol] &= ~(1 << opposite)
        return (ncol, nrow)

    def possible_walls(self, position: tuple[int, int]) -> list[int]:
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
                            if 0 <= ncol < self.width and 0 <= nrow < self.height:
                                if self.maze[nrow][ncol] == 0:
                                    cells_with_walls = False
                                    break
                        if not cells_with_walls:
                            break
                    if cells_with_walls:
                        walls.append(num)
        return walls

    def make_no_perfect(self):
        num_cells = self.width * self.height
        if num_cells < 300:
            cut_cells = math.ceil(0.05 * num_cells)
        elif num_cells < 1000:
            cut_cells = math.ceil(0.1 * num_cells)
        elif num_cells < 3000:
            cut_cells = math.ceil(0.15 * num_cells)
        else:
            cut_cells = 0.20 * num_cells

        solution = SolutionGenerator(self)
        solution.get_solution()
        sol = solution.solution
        num_solutions = len(sol)
        while num_solutions <= 1:
            cells = 0
            while cells < cut_cells:
                position = (random.randint(0, self.width - 1), random.randint(0, self.height -1))
                walls = self.possible_walls(position)
                if walls:
                    wall = random.choice(walls)
                    self.remove_wall((position[0], position[1], wall))
                    cells += 1
            solution = SolutionGenerator(self)
            solution.get_solution()
            sol = solution.solution
            num_solutions = len(sol)

    def gen_maze(self):
        self.visited[self.entry[1], self.entry[0]] = 1
        stack = [(self.entry[0], self.entry[1])]
        while stack:
            col, row = stack[-1]
            walls = self.get_available_walls(col, row)
            if walls:
                wall = random.choice(walls)
                ncol, nrow = self.remove_wall(wall)
                self.visited[nrow, ncol] = 1
                stack.append((ncol, nrow))
            else:
                stack.pop()
        if not self.perfect:
            print("no perfeec")
            self.make_no_perfect()


class SolutionGenerator():

    def __init__(self, maze: MazeGenerator):
        self.maze = maze
        self.solution: list[str] = []
        self.visited = np.full((maze.height, maze.width), 0)

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
        self.visited[self.maze.exit[1], self.maze.exit[0]] = 1
        stack = [[self.maze.exit, [], [self.maze.exit]]]
        while stack:
            position, sol, visited = stack[0]
            if position == self.maze.entry:
                self.solution.append("".join(stack[0][1][::-1]))
            else:
                neighbours = self.get_neighbors(position[0], position[1])
                for x, y, point in neighbours:
                    if (x, y) not in visited:
                        new_sol = sol + [point]
                        new_visited = visited + [(x, y)]
                        stack.append([(x, y), new_sol, new_visited])
            stack.pop(0)


def read_configuration(file_name: str) -> Configuration:
    config_dic: dict[str, Any] = {}
    with open(file_name) as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=')
                key = key.lower()
                if value.isdigit():
                    config_dic[key] = int(value)
                elif ',' in value:
                    config_dic[key] = tuple(map(int, value.split(',')))
                elif value.capitalize() in ['True', 'False']:
                    config_dic[key] = value.capitalize()
                else:
                    config_dic[key] = value
            elif not line.startswith('#'):
                raise ValueError(f"Error in {file_name}: There is a line that"
                                 "does not start with '#' or has the format "
                                 "'KEY=VALUE'")
    config = Configuration(**config_dic)
    return config


def main():
    try:
        config = read_configuration('config.txt')
        maze_1 = MazeGenerator(config)
    except ValueError as e:
        print(f"{e}")
        return
    random.seed(config.seed)
    maze_1.gen_maze()
    solution = SolutionGenerator(maze_1)
    solution.get_solution()
    with open(config.output_file, 'w') as file:
        for row in maze_1.maze:
            line = " ".join([f"{num:X}" for num in row])
            file.write(line)
            file.write('\n')
        file.write(f"\n{maze_1.entry[0]},{maze_1.entry[1]}\n")
        file.write(f"{maze_1.exit[0]},{maze_1.exit[1]}\n")
        file.write(f"{solution.solution[0]}\n")
    
    print(maze_1.maze)
    print(solution.solution)


if __name__ == '__main__':
    main()
