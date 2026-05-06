#! /usr/bin/env python3
import sys



def create_lab() -> None:
    maze = []
    lenlist = len(sys.argv)
    if (lenlist == 1):
        print("Usage:visual.py <file>")
    elif (lenlist > 1):
        try:
            with open(sys.argv[1], 'r') as archivo:
                first_line = archivo.readline().strip()
                first_row = [int(x,16) for x in first_line.split()]
                expected_cols = len(first_row)
                maze.append(first_row)
                for line in archivo:
                    line = line.strip()
                    if not line:
                        break
                    row = [int(x,16) for x in line.split()]
                    if len(row) != expected_cols:
                        raise ValueError(f"Row has wrong length {len(row)}, expected {expected_cols}")
                    maze.append(row)

                entry_line = archivo.readline()
                exit_line = archivo.readline()
                solution = archivo.readline()

                entry_parts = entry_line.strip().split(",")
                entry = []
                for position in entry_parts:
                        entry.append(int(position,10))

                exit_parts = exit_line.strip().split(",")
                exit = []
                for position in exit_parts:
                        exit.append(int(position,10))

                solution = solution.strip().split()

                
                #print(maze)
            screen = []
            for i in range(len(maze)):
                top = []
                mid = []

                for j in range(len(maze[i])):
                    cell = maze[i][j]
                    top.append('+')
                    top.append('---' if cell & 1 else '   ')
                    mid.append('|' if cell & 8 else ' ')
                    mid.append('   ')
                top.append('+')
                mid.append('|')
                screen.append(top)
                screen.append(mid)
            bottom = []

            for j in range(len(maze[0])):
                bottom.append('+')
                bottom.append('---')
            bottom.append('+')
            screen.append(bottom)
           
            screen_i = exit[0]*2 + 1   
            screen_j = exit[0]*4 + 1  
            if 0 <= screen_i < len(screen) and 0 <= screen_j < len(screen[0]):
                screen[screen_i][screen_j] = 'X'

            screen_i = entry[1]*2 + 1
            screen_j = entry[1]*4 + 1
            screen[screen_i][screen_j] = 'O  '
           
            for line in screen :
                print("".join(line) )
            print(f"\n---\nFile '{sys.argv[1]}' closed")
        except PermissionError as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")
        except FileNotFoundError as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")

""" def create_lab() -> None:
    maze = []
    lenlist = len(sys.argv)
    if (lenlist == 1):
        print("Usage:visual.py <file>")
    elif (lenlist > 1):
        try:
            with open(sys.argv[1], 'r') as archivo:
                for line in archivo:
                    if line.strip() == "":
                        break
                    line2 = line.split()
                    row = []
                    for position in line2:
                        row.append(int(position, 16))
                    maze.append(row)
                #print(maze)
            for i in range(len(maze)):
                top = "+"
                mid = ""
                bot = "+"
                for j in range(len(maze[i])):
                    top += "---+" if   maze[i][j] & 1 else "   +"
                    left = "|" if maze[i][j] & 8 else " "
                    bot += "---+" if maze[i][j] & 4 else "   +"
                    if j == len(maze[i])-1:
                        mid += left + "   |"
                    else:
                        mid += left + "   "
                
                print(top)
                print(mid)
            print(bot)
            screen = []
            screen.append(top)
            screen.append(mid)
            screen[row][line] = 'O'
            print(f"\n---\nFile '{sys.argv[1]}' closed")
        except PermissionError as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")
        except FileNotFoundError as e:
            print(f"Error opening file '{sys.argv[1]}': {e}")
 """

if __name__ == "__main__":
    create_lab()