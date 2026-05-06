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
    width: int = Field(..., ge=2)
    height: int = Field(..., ge=2)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool

    @model_validator(mode='after')
    def check_rules(self) -> Self:
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
        
        return(self)


class MazeGenerator():

    def __init__(self, maze_data: Configuration):
        self.width = maze_data.width
        self.height = maze_data.height
        self.entry = maze_data.entry
        self.exit = maze_data.exit
        self.maze = np.full((maze_data.height, maze_data.width), 15)
        self.position = list(maze_data.entry)
        self.visited = np.full((maze_data.height, maze_data.width), 0)
        self.solution = ""
        self.write_42()


    def get_neighbors(self) -> list:
        walls = []
        dirs = [
                    (-1, 0, 0, 2),  # west
                    (0, 1, 1, 3),   # south
                    (1, 0, 2, 0),   # east
                    (0, -1, 3, 1)   # north
        ]
        x, y = self.position
        for dir in dirs:
            if (0 <= (x + dir[0]) < self.width and
                    0 <= (y + dir[1]) < self.height and
                    self.visited[y + dir[1], x + dir[0]] == 0):
                walls.append((x + dir[0], y + dir[1], dir[2], dir[3], x, y))
        return walls

    def remove_wall(self, neighbor: tuple):
        nx, ny, wall, opposite, x, y= neighbor
        self.visited[y, x] = 1

        self.maze[y, x] &= ~(1 << wall)
        self.maze[ny, nx] &= ~(1 << opposite)
        self.position = [nx, ny]

    def write_42(self):
        if self.height >= 8 and self.width >= 10:
            x = int(self.width / 2)
            y = int(self.height / 2)
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
            self.visited[y - 1, x + 3,] = 42

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

    def gen_maze(self, sol: list | None = None):
        if sol is None:
            sol = []
        self.visited[self.position[1], self.position[0]] = 1
        walls = self.get_neighbors()
        while walls:
            if self.all_visited():
                return
            self.visited[self.position[1], self.position[0]] = 1
            remove = random.randint(0, len(walls) - 1) 
            if self.visited[walls[remove][1], walls[remove][0]] == 1:
                walls.pop(remove)
            else:
                self.remove_wall(walls[remove])
                sol.append(self.transform_dir(walls[remove][2]))
                if self.position == list(self.exit):
                    self.solution = "".join(sol)
                walls.pop(remove)
                self.gen_maze(sol)
            if sol:
                sol.pop()


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
        file.write(f"\n{maze_1.solution}\n")


if __name__ == '__main__':
    main()
