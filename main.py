from maze import (Configuration, SolutionGenerator, MazeGenerator,
                  ValidationError, random)
from typing import Any


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
        maze = MazeGenerator(config)
    except (ValueError, ValidationError) as e:
        print(f"{e}")
        return
    random.seed(config.seed)
    maze.gen_maze()
    solution = SolutionGenerator(maze)
    solution.get_solution()
    with open(config.output_file, 'w') as file:
        for row in maze.maze:
            line = " ".join([f"{num:X}" for num in row])
            file.write(line)
            file.write('\n')
        file.write(f"\n{maze.entry[0]},{maze.entry[1]}\n")
        file.write(f"{maze.exit[0]},{maze.exit[1]}\n")
        file.write(f"{solution.solution[0]}\n")

    print(maze.maze)
    print(solution.solution)


if __name__ == '__main__':
    main()
