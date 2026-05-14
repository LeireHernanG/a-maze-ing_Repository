from generator import MazeGenerator
import random
from typing import Any
from prueba import menu


def read_configuration(file_name: str) -> dict[str, Any]:
    config_dic: dict[str, Any] = {}
    with open(file_name) as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=')
                key = key.upper()
                if key == 'OUTPUT_FILE':
                    if not value:
                        raise ValueError(f"'Missing value for '{key}'")
                    config_dic[key] = value
                elif key == 'PERFECT':
                    if value.upper() == 'TRUE':
                        config_dic[key] = True
                    elif value.upper() == 'FALSE':
                        config_dic[key] = False
                    else:
                        raise ValueError(
                            f"The parameter '{key}' must be true or false"
                        )
                elif key in ['ENTRY', 'EXIT']:
                    try:
                        config_dic[key] = tuple(map(int, value.split(',')))
                    except ValueError:
                        raise ValueError(
                            f"The parameter '{key}' must be 'int,int'")
                    if len(config_dic[key]) != 2:
                        raise ValueError(
                            f"The parameter '{key}' must be 'int,int'")
                else:
                    if not value.isdigit():
                        raise ValueError(
                            f"The parameter '{key}' must an Integer")
                    config_dic[key] = int(value)

            elif not line.startswith('#'):
                raise ValueError(
                    f"Error in '{file_name}': There is a line that"
                    "does not start with '#' or has the format "
                    "'KEY=VALUE'")
    if 'SEED' not in config_dic.keys():
        config_dic['SEED'] = 42
    key_words = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for word in key_words:
        if word not in config_dic.keys():
            raise ValueError(
                f"the parameter '{word}' is missing in '{file_name}'")
    return config_dic


def main(option_is_one: bool | None = None) -> Any:
    try:
        config = read_configuration('config.txt')
        if option_is_one:
            random.seed(random.randint(0, 1000))
            config['SEED'] = random.randint(0, 1000)
        maze = MazeGenerator(
                                width=config['WIDTH'],
                                height=config['HEIGHT'],
                                entry=config['ENTRY'],
                                exit=config['EXIT'],
                                perfect=config['PERFECT'],
                                seed=config['SEED']
        )
    except ValueError as e:
        raise ValueError(e)
    random.seed(maze.seed)
    maze.gen_maze()
    with open(config['OUTPUT_FILE'], 'w') as file:
        for row in maze.structure:
            line = " ".join([f"{num:X}" for num in row])
            file.write(line)
            file.write('\n')
        file.write(f"\n{maze.entry[0]},{maze.entry[1]}\n")
        file.write(f"{maze.exit[0]},{maze.exit[1]}\n")
        file.write(f"{maze.solution[0]}\n")
    return config['OUTPUT_FILE']


if __name__ == '__main__':
    try:
        filename = main()
        option = menu(filename)
        while option > 0:
            if option == 1:
                main(True)
            option = menu(filename)
    except ValueError as e:
        print(f"Couldn't make the maze:{e}")
