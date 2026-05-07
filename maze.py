import numpy as np
import random
from pydantic import (BaseModel, Field, ValidationError, model_validator)
from typing import Any
from typing_extensions import Self


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
        return self


class MazeGenerator():

    def __init__(self, maze_data: Configuration):
        self.width = maze_data.width
        self.height = maze_data.height
        self.entry = maze_data.entry
        self.exit = maze_data.exit
        self.maze = np.full((maze_data.height, maze_data.width), 15)
        self.visited = np.full((maze_data.height, maze_data.width), 0)
        self.write_42()

    def get_neighbors(self, col: int, row: int) -> list:
        walls = []
        dirs = [
                    (-1, 0, 3, 1),  # west
                    (0, 1, 2, 0),   # south
                    (1, 0, 1, 3),   # east
                    (0, -1, 0, 2)   # north
        ]
        for dir in dirs:
            if (0 <= (col + dir[0]) < self.width and
                    0 <= (row + dir[1]) < self.height and
                    self.visited[row + dir[1], col + dir[0]] == 0):
                walls.append((col + dir[0], row + dir[1], dir[2], dir[3], col, row))
        return walls

    def remove_wall(self, neighbor: tuple):
        ncol, nrow, wall, opposite, col, row = neighbor

        self.maze[row, col] &= ~(1 << wall)
        self.maze[nrow, ncol] &= ~(1 << opposite)

    def write_42(self):
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
                    self.visited[y0 + y, x0 + x] = 1

    def gen_maze(self):
        self.visited[self.entry[1], self.entry[0]] = 1
        stack = [(self.entry[0], self.entry[1])]
        while stack:
            col, row = stack[-1]
            walls = self.get_neighbors(col, row)
            if walls:
                wall = random.choice(walls)
                ncol, nrow = wall[0], wall[1]
                self.remove_wall(wall)
                self.visited[nrow, ncol] = 1
                stack.append((ncol, nrow))
            else:
                stack.pop()


class SolutionGenerator():

    def __init__(self, maze: MazeGenerator):
        self.maze = maze
        self.solution = ''
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
                x, y, point  = dirs[num]
                nx, ny = col + x, row + y
                if self.visited[ny, nx] == 0:
                    self.visited[ny, nx] = 1
                    neighbors.append((nx, ny, point))
        return neighbors

    def get_solution(self):
        self.visited[self.maze.exit[1], self.maze.exit[0]] = 1
        stack = [[self.maze.exit, []]]
        while True:
            position, sol = stack[0]
            if position == self.maze.entry:
                break
            neighbours = self.get_neighbors(position[0], position[1])
            for neighbour in neighbours:
                x, y, point = neighbour
                new_sol = sol + [point]
                stack.append([(x, y), new_sol])
            stack.pop(0)
        self.solution = "".join(stack[0][1][::-1])



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
        file.write(f"\n{solution.solution}\n")
    
    print(solution.visited)
    print(solution.solution)


if __name__ == '__main__':
    main()
