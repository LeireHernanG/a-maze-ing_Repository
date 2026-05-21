from mazegen import MazeGenerator
import random
from typing import Any
from visual import menu


def read_configuration(file_name: str) -> dict[str, Any]:
    """
    Reads and parses a configuration file for the maze generator.

    The file must contain key-value pairs in the
    format 'KEY=VALUE', one per line.
    Lines starting with '#' are treated as comments and ignored.

    Supported keys:
        - WIDTH: int, maze width
        - HEIGHT: int, maze height
        - ENTRY: tuple[int, int], entry coordinates (x,y)
        - EXIT: tuple[int, int], exit coordinates (x,y)
        - OUTPUT_FILE: str, output file name
        - PERFECT: bool, whether the maze is perfect or not
        - SEED: optional int, random seed (defaults to 42 if missing)

    Validation rules:
        - WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, and PERFECT are mandatory
        - WIDTH and HEIGHT must be integers
        - ENTRY and EXIT must be in the format 'int,int'
        - PERFECT must be 'true' or 'false'
        - SEED, if present, must be an integer

    Args:
        file_name (str): Path to the configuration file.

    Returns:
        dict[str, Any]: Dictionary containing the parsed configuration.

    Raises:
        ValueError: If the file format is invalid or required
        parameters are missing.
    """
    config_dic: dict[str, Any] = {}
    with open(file_name) as file:
        for line in file:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=')
                key = key.strip().upper()
                value = value.strip()
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
                        config_dic[key] = tuple(
                            map(lambda x: int(x.strip()), value.split(',')))
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


def validate(config: dict[str, Any]) -> None:
    """
    Validates maze configuration values
    and ensures they are within valid bounds.

    This function checks that:
        - WIDTH and HEIGHT are between 3 and 100 inclusive
        - ENTRY coordinates are within maze bounds
        - EXIT coordinates are within maze bounds

    Args:
        config (dict[str, Any]): Configuration dictionary produced by
        read_configuration().

    Raises:
        ValueError: If any parameter is out of allowed bounds or invalid.
    """

    if not (2 < config['WIDTH'] < 101):
        raise ValueError('The width must be between 2 and 100')
    if not (2 < config["HEIGHT"] < 101):
        raise ValueError('The height must be between 2 and 100')
    if not (0 <= config["ENTRY"][0] < config['WIDTH']):
        raise ValueError('The entry x position is out of bounds')
    if not (0 <= config["ENTRY"][1] < config["HEIGHT"]):
        raise ValueError('The entry y position is out of bounds')
    if not (0 <= config["EXIT"][0] < config['WIDTH']):
        raise ValueError('The exit x position is out of bounds')
    if not (0 <= config["EXIT"][1] < config["HEIGHT"]):
        raise ValueError('The exit y position is out of bounds')


def main(option_is_one: bool | None = None) -> Any:
    """
    Main execution function for generating and exporting a maze.

    This function:
        1. Reads configuration from 'config.txt'
        2. Validates the configuration
        3. Optionally randomizes the seed if option_is_one is True
        4. Generates a maze using MazeGenerator
        5. Writes the maze structure, entry/exit, and solution to a file
        6. Returns the output file name

    If option_is_one is True, the random seed is regenerated randomly.

    Args:
        option_is_one (bool | None): If True, forces a new random
        seed generation.

    Returns:
        Any: The name of the generated output file.

    Raises:
        ValueError: If configuration reading or validation fails.
    """
    try:
        config = read_configuration('config.txt')
        validate(config)
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
            line = "".join([f"{num:X}" for num in row])
            file.write(line)
            file.write('\n')
        file.write(f"\n{maze.entry[0]},{maze.entry[1]}\n")
        file.write(f"{maze.exit[0]},{maze.exit[1]}\n")
        file.write(f"{maze.solution}\n")
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
