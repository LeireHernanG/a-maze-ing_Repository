import numpy as np
import random

# north = 3
# east = 2
# south = 1
# west = 0

class MazeGenerator():

    def __init__(self, width: int, heigth: int, entry: tuple[int, int],
                 exit: tuple[int, int]):
        self.width = width
        self.heigth = heigth
        self.entry = entry
        self.exit = exit
        self.maze = np.full((heigth, width), 15)
        self.position = list(entry)
        self.visited = np.full((heigth, width), 0)
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
                    0 <= (y + dir[1]) < self.heigth and
                    self.visited[y + dir[1], x + dir[0]] == 0):
                walls.append((x + dir[0], y + dir[1], dir[2], dir[3], x, y))
        return walls

    def remove_wall(self, neighbor: tuple):
        nx, ny, wall, opposite, x, y= neighbor
        self.visited[y, x] = 1

        self.maze[y, x] &= ~(1 << wall)
        self.maze[ny, nx] &= ~(1 << opposite)
        # print(f"wall: {wall}, x: {x}, y:{y}, num = {self.maze[y, x]}")
        # print(f"opposite: {opposite}, nx: {nx}, ny:{ny}, num = {self.maze[ny, nx]}")
        # print(self.maze)
        self.position = [nx, ny]

    def write_42(self):
        if self.heigth >= 8 and self.width >= 10:
            x = int(self.width / 2)
            y = int(self.heigth / 2)
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

    def gen_maze(self):
        self.visited[self.position[1], self.position[0]] = 1
        walls = self.get_neighbors()
        print(self.position)
        print(walls)
        while walls:
            if self.all_visited():
                return
            self.visited[self.position[1], self.position[0]] = 1
            remove = random.randint(0, len(walls) - 1)
            if self.visited[walls[remove][1], walls[remove][0]] == 1:
                walls.pop(remove)
            else:
                print(f"pared: {walls[remove]}")
                self.remove_wall(walls[remove])
                walls.pop(remove)
                # print(self.maze)
                # print(self.visited)
                # print(self.position)
                self.gen_maze()



def main():
    random.seed(123)
    maze_1 = MazeGenerator(10, 20,(0, 1), (3, 3))
    maze_1.gen_maze()
    print(maze_1.maze)


if __name__ == '__main__':
    main()
