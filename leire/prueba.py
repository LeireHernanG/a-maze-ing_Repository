import sys
import os
from maze import MazeGenerator
#from pydantic import ValidationError
import random
from typing import Any
from colorama import init, Fore, Back, Style
import time

path = {
    "show_path": False
}
colors = {
    "wall": "#29a93e",
    "path": "#ffffff",
    "corners":"#bef14b",
    "exit_icon_back":"#c91f1f",
    "entry_icon_back":"#0026FF",
    "exit_icon_fore":"#ffffff",
    "entry_icon_fore":"#ffffff",
    "42":"#f2b603"
}


    
def menu(output_file:str) -> int:
        create_lab(output_file)
        print(Style.BRIGHT + Fore.BLUE +"\n⭐▁ ▂ ▃ ▅ ▆ ▇ ▌ A-Maze-Ing ▐ ▇ ▆ ▅ ▃ ▂ ▁⭐​")
        print("\n1. Regenerate a new maze 🔄​\n2. Show/Hide path from entry to exit ​👁️‍🗨️​\n3. Rotate maze colors​ 🔴​🟢​🔵​\n4. Quit ​⛔​")
        valor = input("\n-Select an option? (1-4): ").strip()

        if not valor.isdigit():
            return 5

        valor = int(valor)
        if valor == 1:
            return 1
        elif valor == 2:
            path["show_path"] = not path["show_path"]
            return 2
        elif valor == 3:
            print("\n=== Rotate maze colors ===")
            print("1. Mario bros")
            print("2. Space")
            print("3. Hot pink")
            theme = input("Choose theme: ").strip()
            if not theme.isdigit():
                return 4
            theme = int(theme)
            if theme == 1:
                colors["wall"]= "#29a93e"
                colors["path"]= "#ffffff"
                colors["corners"]="#bef14b"
                colors["exit_icon_back"]="#c91f1f"
                colors["entry_icon_back"]="#A2FF92"
                colors["exit_icon_fore"]="#ffffff"
                colors["entry_icon_fore"]="#ffffff"
                colors["42"]="#f2b603"

            elif theme == 2:
                colors["wall"] = "#0984ff"
                colors["corners"] = "#ffec1d"
                colors["entry_icon_back"]="#86ff62"
                colors["exit_icon_back"]="#ff5d5d"
                colors["exit_icon_fore"]="#FFFFFF"
                colors["42"]="#ffffff"
                colors["path"]= "#ffea00"
                
            elif theme == 3:
                colors["wall"] = "#00ffd0"
                colors["corners"] = "#0d0de7"
                colors["entry_icon_back"]="#d8e829"
                colors["entry_icon_fore"]="#5E005F"
                colors["exit_icon_back"]="#c431f9"
                colors["exit_icon_fore"]="#FFFFFF"
                colors["path"]= "#ffff00"
                colors["42"]="#f10d51"
            #create_lab(output_file)
            return 3
        elif valor == 4:
            print("Good bye!")
            return 0
        else:
            print("Invalid number")
            return 5
        


def create_lab(output_file:str) -> None:
    if len(sys.argv) == 1:
        print("Usage: prueba.py <file>")
        return

    try:
        with open(output_file, 'r') as archivo:
            maze = []
            for line in archivo:
                line = line.strip()
                if line == "":
                    break
                maze.append([int(x, 16) for x in line.split()])
            if not maze:
                print("Error: Laberinto vacío")
                return

            rows = len(maze)
            cols = len(maze[0])
            entry = [int(x) for x in archivo.readline().strip().split(",")]
            exit = [int(x) for x in archivo.readline().strip().split(",")]
            solution = archivo.readline().strip()
        
        os.system("clear")
        screen = []

        for i in range(rows):
            top = []
            for j in range(cols):
                cell = maze[i][j]
                if cell == 15:
                    top.append(imprimir_color('¤',colors["corners"],colors["42"]))
                    top.append(imprimir_color('═══', colors["42"],colors["42"]))
                else:
                    top.append(imprimir_color('¤',colors["corners"]))
                    top.append(imprimir_color('═══',colors["wall"]) if (cell & 1 or (i > 0 and maze[i-1][j] & 4)) else '   ')
            top.append(imprimir_color('¤',colors["corners"]))
            screen.append(top)
            
            mid = []
            for j in range(cols):
                cell = maze[i][j]
                if cell == 15:
                    mid.append(imprimir_color('║',  colors["42"],colors["42"]))
                    mid.append(imprimir_color('   ', colors["42"],colors["42"]))
                else:
                    mid.append(imprimir_color('║',colors["wall"]) if (cell & 8 or (j > 0 and maze[i][j-1] & 2)) else ' ')
                    mid.append('   ')
            mid.append(imprimir_color('║',colors["wall"]) if (maze[i][cols-1] & 2) else ' ')
            screen.append(mid)

        bottom = []
        for j in range(cols):
            cell = maze[i][j]
            if cell == 15:
                bottom.append(imprimir_color('¤', colors["wall"],colors["wall"]))
                bottom.append(imprimir_color('═══',  colors["wall"],colors["wall"]))
            else:
                bottom.append(imprimir_color('¤',colors["corners"]))
                bottom.append(imprimir_color('═══',colors["wall"]) if (cell & 4 or (i+1 < rows and maze[i+1][j] & 1)) else '   ')
        bottom.append(imprimir_color('¤',colors["corners"]))
        screen.append(bottom)

        full_width = cols * 4 + 1
        for row in screen:
            while len(row) < full_width:
                row.append(' ')

        row_idx = entry[0]*2 + 1
        col_idx = entry[1]*2 + 1  
        screen[col_idx][row_idx] = imprimir_color(' O ', colors["entry_icon_fore"], colors["entry_icon_back"])

        row_idx = exit[0]*2 + 1
        col_idx = exit[1]*2 + 1
        screen[col_idx][row_idx] = imprimir_color(' X ',colors["exit_icon_fore"], colors["exit_icon_back"])

        if path["show_path"]:
            solution_path(entry, screen, exit, solution)
        else:
            for line in screen:
                print("".join(line))

    except PermissionError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
    except FileNotFoundError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")


def solution_path(entry, screen,exit, solution):
    row_indx = entry[1]
    col_idx = entry[0]
    for paso in solution:
        if paso == 'N':
            row_indx -= 1
        elif paso == 'S':
            row_indx += 1
        elif paso == 'E':
            col_idx += 1
        elif paso == 'W':
            col_idx -= 1
        
        visual_row = row_indx * 2 + 1
        visual_col = col_idx * 2 + 1

        if row_indx == exit[1] and col_idx == exit[0]:
            return
        else:
            screen[visual_row][visual_col] = imprimir_color(' + ',colors["path"])

            print("\033[H\033[J", end="")
            for line in screen:
                print("".join(line))
            time.sleep(0.05)


def imprimir_color(texto, fg_hex=None, bg_hex=None):
    seq = ""
    if fg_hex:
        r, g, b = int(fg_hex[1:3], 16), int(fg_hex[3:5], 16), int(fg_hex[5:7], 16)
        seq += f"\033[38;2;{r};{g};{b}m"
    if bg_hex:
        r, g, b = int(bg_hex[1:3], 16), int(bg_hex[3:5], 16), int(bg_hex[5:7], 16)
        seq += f"\033[48;2;{r};{g};{b}m"
    return f"{seq}{texto}{Style.RESET_ALL}"
                     
if __name__ == "__main__":
    menu()