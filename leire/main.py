from maze import MazeGenerator
from pydantic import ValidationError
import random
from typing import Any
import sys
from prueba import menu

def read_configuration(file_name: str) -> dict:
    config_dic: dict[str, Any] = {}
    with open(file_name) as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=')
                key = key.upper()
                if value.isdigit():
                    config_dic[key] = int(value)
                elif ',' in value:
                    config_dic[key] = tuple(map(int, value.split(',')))
                elif value.upper() == 'TRUE':
                    config_dic[key] = True
                elif value.upper() == 'FALSE':
                    config_dic[key] = False
                else:
                    config_dic[key] = value
            elif not line.startswith('#'):
                raise ValueError(f"Error in {file_name}: There is a line that"
                                 "does not start with '#' or has the format "
                                 "'KEY=VALUE'")
    if 'SEED' not in config_dic.keys():
        config_dic['SEED'] = 42
    return config_dic


def main(seed:bool|None=None) -> str:
    error = 0
    try:
        config = read_configuration('config.txt')
        if seed:
            config['SEED']= random.randint(0,100)
        maze = MazeGenerator(
                                width=config['WIDTH'],
                                height=config['HEIGHT'],
                                entry=config['ENTRY'],
                                exit=config['EXIT'],
                                output_file=config['OUTPUT_FILE'],
                                perfect=config['PERFECT'],
                                seed=config['SEED']
        )
    except (ValueError, ValidationError) as e:
        raise ValueError(f"{e}")
    random.seed(maze.seed)
    maze.gen_maze()
    with open(maze.output_file, 'w') as file:
        for row in maze.maze:
            line = " ".join([f"{num:X}" for num in row])
            file.write(line)
            file.write('\n')
        file.write(f"\n{maze.entry[0]},{maze.entry[1]}\n")
        file.write(f"{maze.exit[0]},{maze.exit[1]}\n")
        file.write(f"{maze.solution[0]}\n")
    return(config['OUTPUT_FILE'])


if __name__ == '__main__':
    try:
        filename=main()
        option =menu(filename)
        while option >0:
            if option == 1:
                main(True)
            option = menu(filename)
    except Exception as e:
        print(f"Couldn't make the maze:{e}")