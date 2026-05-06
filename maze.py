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
        self.position = list(maze_data.entry)
        self.visited = np.full((maze_data.height, maze_data.width), 0)
        self.write_42()


    def get_neighbors(self, x: int, y: int) -> list:
        walls = []
        dirs = [
                    (-1, 0, 3, 1),  # west
                    (0, 1, 2, 0),   # south
                    (1, 0, 1, 3),   # east
                    (0, -1, 0, 2)   # north
        ]
        for dir in dirs:
            if (0 <= (x + dir[0]) < self.width and
                    0 <= (y + dir[1]) < self.height and
                    self.visited[y + dir[1], x + dir[0]] == 0):
                walls.append((x + dir[0], y + dir[1], dir[2], dir[3], x, y))
        return walls

    def remove_wall(self, neighbor: tuple):
        nx, ny, wall, opposite, x, y= neighbor

        self.maze[y, x] &= ~(1 << wall)
        self.maze[ny, nx] &= ~(1 << opposite)

    def write_42(self):

        # x0 = self.width // 2 - len(pattern[0]) // 2
        # y0 = self.height // 2 - len(pattern) // 2
        # pattern = [
        #     '1   111'
        #     '1     1'
        #     '111 111'
        #     '  1 1  '
        #     '  1 111'
        # ]
        # for y, row in enumerate(pattern)
        if self.height >= 8 and self.width >= 10:
            x = self.width // 2
            y = self.height // 2
            for cell in range(1, 4):
                self.visited[y, x + cell] = 42
                self.visited[y, x - cell] = 42
            for cell in range(1, 3):
                self.visited[y - cell, x - 3] = 42
                self.visited[y + cell, x - 1] = 42  
            for cell in range(1, 4):
                self.visited[y + 2, x + cell] = 42
                self.visited[y - 2, x + cell] = 42
            self.visited[y + 1, x + 1] = 42
            self.visited[y - 1, x + ] = 42

    def all_visited(self):
        return (all(elem in (1, 42) for row in self.visited for elem in row))
    
    def transform_dir(self, dir: int) -> str:
        if dir == 0:
            return('W')
        elif dir == 1:
            return 'S'
        elif dir == 2:
            return 'E'
        else:
            return 'N'

    def gen_maze(self, x: int | None = None, y: int | None = None):
        if x is None:
            x = self.entry[0]
        if y is None:
            y = self.entry[1]
        self.visited[y, x] = 1
        walls = self.get_neighbors(x, y)
        while walls:
            wall = walls.pop(random.randint(0, len(walls) - 1))
            nx, ny = wall[0], wall[1]
            if self.visited[ny, nx] == 0:
                self.remove_wall(wall)
                self.gen_maze(nx, ny)



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
                    config_dic[key]  = value
            elif not line.startswith('#'):
                raise ValueError(f"Error in {file_name}: There is a line that does not start with '#' or has the format 'KEY=VALUE'")
                
    config = Configuration(**config_dic)
    return config

def main():
    random.seed(123)
    try:
        config = read_configuration('config.txt')
        maze_1 = MazeGenerator(config)
    except ValueError as e:
        print(f"{e}")
        return
    maze_1.gen_maze()
    with open(config.output_file, 'w') as file:
        for row in maze_1.maze:
            line = " ".join([f"{num:X}" for num in row])
            file.write(line)
            file.write('\n')
        file.write(f"\n{maze_1.entry[0]},{maze_1.entry[1]}\n")
        file.write(f"{maze_1.exit[0]},{maze_1.exit[1]}\n")
        print(maze_1.visited)
        #file.write(f"\n{maze_1.solution}\n")


if __name__ == '__main__':
    main()
