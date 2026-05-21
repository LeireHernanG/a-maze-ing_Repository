import sys
import os
import time
import random

path = {"show_path": False, "animated": False}


colors = {
    "wall": "#29a93e",
    "path": "#ffffff",
    "corners": "#bef14b",
    "exit_icon_back": "#c91f1f",
    "entry_icon_back": "#0026FF",
    "exit_icon_fore": "#ffffff",
    "entry_icon_fore": "#ffffff",
    "42": "#f2b603",
}


def print_menu() -> None:
    print("\033[1;34m\n⭐▁ ▂ ▃ ▅ ▆ ▇ ▌ A-Maze-Ing ▐ ▇ ▆ ▅ ▃ ▂ ▁⭐​")
    print(
        "\n1. Regenerate a new maze 🔄​"
        "\n2. Show/Hide path from entry to exit 👁️‍🗨️​"
        "\n3. Rotate maze colors 🔴🟢🔵"
        "\n4. Rotate 42 colors 🟢🔵"
        "\n5. Quit ⛔"
    )


def menu(output_file: str) -> int:
    """
    Display the interactive maze menu and handle user options.

    This function renders the maze, shows the available menu actions,
    and processes the user's selection. It also allows toggling the
    solution path visibility and changing the maze color theme.

    Args:
        output_file (str): Path to the maze file to be displayed.

    Returns:
        int:
            - 0: Exit program
            - 1: Regenerate maze
            - 2: Toggle path visibility
            - 3: Change maze colors
            - 4: Invalid theme selection
            - 5: Invalid menu option
    """

    create_lab(output_file)
    print_menu()

    valor_str: str = input("\n-Select an option? (1-5): ").strip()

    if not valor_str.isdigit():
        return 6

    valor = int(valor_str)
    if valor == 1:
        return 1

    elif valor == 2:
        path["show_path"] = not path["show_path"]

        if not path["show_path"]:
            path["animated"] = False
        return 2

    elif valor == 3:
        print("\n=== Rotate maze colors ===")
        print("1. Mario bros")
        print("2. Space")
        print("3. Hot pink")

        theme_str = input("Choose theme: ").strip()
        if not theme_str.isdigit():
            return 4

        theme = int(theme_str)

        if theme == 1:
            colors["wall"] = "#29a93e"
            colors["path"] = "#ffffff"
            colors["corners"] = "#bef14b"
            colors["exit_icon_back"] = "#c91f1f"
            colors["entry_icon_back"] = "#0026FF"
            colors["exit_icon_fore"] = "#ffffff"
            colors["entry_icon_fore"] = "#ffffff"
            colors["42"] = "#f2b603"

        elif theme == 2:
            colors["wall"] = "#0984ff"
            colors["corners"] = "#ffec1d"
            colors["entry_icon_back"] = "#86ff62"
            colors["exit_icon_back"] = "#ff5d5d"
            colors["exit_icon_fore"] = "#FFFFFF"
            colors["42"] = "#ffffff"
            colors["path"] = "#ffea00"

        elif theme == 3:
            colors["wall"] = "#00ffd0"
            colors["corners"] = "#0d0de7"
            colors["entry_icon_back"] = "#d8e829"
            colors["entry_icon_fore"] = "#5E005F"
            colors["exit_icon_back"] = "#c431f9"
            colors["exit_icon_fore"] = "#FFFFFF"
            colors["path"] = "#ffff00"
            colors["42"] = "#f10d51"
        return 3

    elif valor == 4:
        colors["42"] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        return 4

    elif valor == 5:
        print("Good bye!")
        return 0

    else:
        print("Invalid number")
        return 6


def create_lab(output_file: str) -> None:
    """
    Read a maze file and render the maze in the terminal.

    The function parses the maze structure, entry and exit positions,
    and optional solution path from the specified file. It then draws
    the maze using colored terminal characters.

    Args:
        output_file (str): Path to the maze file.

    Returns:
        None
    """
    if len(sys.argv) == 1:
        print("Usage: prueba.py <file>")
        return

    try:
        with open(output_file, "r") as archivo:
            maze = []

            for line in archivo:
                line = line.strip()
                if line == "":
                    break
                maze.append([int(x, 16) for x in line])

            if not maze:
                print("Error: Laberinto vacío")
                return

            rows = len(maze)
            cols = len(maze[0])
            entry = [int(x) for x in archivo.readline().strip().split(",")]
            exit = [int(x) for x in archivo.readline().strip().split(",")]
            solution = archivo.readline().strip()

        os.system("clear")
        print("\033[H", end="")
        screen: list[list[str]] = []

        for i in range(rows):
            top: list[str] = []
            for j in range(cols):
                cell = maze[i][j]
                if cell == 15:
                    top.append(print_color("¤", colors["corners"],
                                           colors["42"]))
                    top.append(print_color("═══", colors["42"],
                                           colors["42"]))
                else:
                    top.append(print_color("¤", colors["corners"]))
                    top.append(
                        print_color("═══", colors["wall"])
                        if (cell & 1 or (i > 0 and maze[i - 1][j] & 4))
                        else "   "
                    )

            top.append(print_color("¤", colors["corners"]))
            screen.append(top)
            mid: list[str] = []

            for j in range(cols):
                cell = maze[i][j]
                if cell == 15:
                    mid.append(print_color("║", colors["42"], colors["42"]))
                    mid.append(print_color("   ", colors["42"], colors["42"]))
                else:
                    mid.append(
                        print_color("║", colors["wall"])
                        if (cell & 8 or (j > 0 and maze[i][j - 1] & 2))
                        else " "
                    )
                    mid.append("   ")

            mid.append(
                print_color("║", colors["wall"])
                if (maze[i][cols - 1] & 2) else " "
            )
            screen.append(mid)

        bottom: list[str] = []

        for j in range(cols):
            cell = maze[i][j]
            if cell == 15:
                bottom.append(print_color("¤",
                                          colors["wall"], colors["wall"]))
                bottom.append(print_color("═══",
                                          colors["wall"], colors["wall"]))
            else:
                bottom.append(print_color("¤", colors["corners"]))
                bottom.append(
                    print_color("═══", colors["wall"])
                    if (cell & 4 or (i + 1 < rows and maze[i + 1][j] & 1))
                    else "   "
                )

        bottom.append(print_color("¤", colors["corners"]))
        screen.append(bottom)

        full_width = cols * 4 + 1
        for row in screen:
            while len(row) < full_width:
                row.append(" ")

        row_idx = entry[0] * 2 + 1
        col_idx = entry[1] * 2 + 1
        screen[col_idx][row_idx] = print_color(
            " O ", colors["entry_icon_fore"], colors["entry_icon_back"]
        )

        row_idx = exit[0] * 2 + 1
        col_idx = exit[1] * 2 + 1
        screen[col_idx][row_idx] = print_color(
            " X ", colors["exit_icon_fore"], colors["exit_icon_back"]
        )

        if len(solution) > 1 and path["show_path"]:
            solution_path(entry, screen, exit, solution,
                          animate=not path["animated"])
            path["animated"] = True

        print("\033[H", end="")

        if rows < 8 or cols < 10:
            print("\033[1;34mThere is no space for '42' pattern.")

        for line_map in screen:
            print("".join(line_map))

    except PermissionError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
    except FileNotFoundError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")


def solution_path(
    entry: list[int], screen: list[list[str]],
    exit: list[int], solution: str, animate: bool = True
) -> None:
    """
    Animate and display the solution path inside the maze.

    The function follows the sequence of movements stored in the
    solution string and updates the maze display step by step
    until the exit is reached.

    Args:
        entry (list): Starting coordinates of the maze entry.
        screen (list): Matrix representing the rendered maze.
        exit (list): Coordinates of the maze exit.
        solution (str): Sequence of directions ('N', 'S', 'E', 'W').

    Returns:
        None
    """
    row_indx = entry[1]
    col_idx = entry[0]

    for paso in solution:
        if paso == "N":
            row_indx -= 1
        elif paso == "S":
            row_indx += 1
        elif paso == "E":
            col_idx += 1
        elif paso == "W":
            col_idx -= 1

        visual_row = row_indx * 2 + 1
        visual_col = col_idx * 2 + 1

        if row_indx == exit[1] and col_idx == exit[0]:
            break
        else:
            screen[visual_row][visual_col] = print_color(" + ", colors["path"])

        if animate:
            print("\033[H", end="")
            for line in screen:
                print("".join(line))
            print_menu()
            time.sleep(0.02)

    if not animate:
        print("\033[H", end="")
        for line in screen:
            print("".join(line))


def print_color(
    texto: str, fg_hex: str | None = None, bg_hex: str | None = None
) -> str:
    """
    Apply ANSI foreground and background colors to a text string.

    Converts hexadecimal color values into ANSI escape sequences
    to display colored text in the terminal.

    Args:
        texto (str): Text to colorize.
        fg_hex (str, optional): Foreground color in hexadecimal format.
        bg_hex (str, optional): Background color in hexadecimal format.

    Returns:
        Any: Colored string formatted with ANSI escape codes.
    """
    seq = ""
    if fg_hex:
        r, g, b = (int(fg_hex[1:3], 16),
                   int(fg_hex[3:5], 16),
                   int(fg_hex[5:7], 16))
        seq += f"\033[38;2;{r};{g};{b}m"

    if bg_hex:
        r, g, b = (int(bg_hex[1:3], 16),
                   int(bg_hex[3:5], 16),
                   int(bg_hex[5:7], 16))
        seq += f"\033[48;2;{r};{g};{b}m"

    return f"{seq}{texto}\033[0m"
