import sys


def create_lab() -> None:

    if len(sys.argv) == 1:
        print("Usage: visual.py <file>")
        return

    try:
        with open(sys.argv[1], 'r') as archivo:
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

        screen = []

        for i in range(rows):
            top = []
            for j in range(cols):
                cell = maze[i][j]
                if cell == 15:
                    top.append(imprimir_color('¤',"#bef14b","#f2b603"))
                    top.append(imprimir_color('═══', "#f2b603","#f2b603"))
                else:
                    top.append(imprimir_color('¤',"#bef14b"))
                    top.append(imprimir_color('═══',"#29a93e") if (cell & 1 or (i > 0 and maze[i-1][j] & 4)) else '   ')
            top.append(imprimir_color('¤',"#bef14b"))
            screen.append(top)
            
            mid = []
            for j in range(cols):
                cell = maze[i][j]
                if cell == 15:
                    mid.append(imprimir_color('║',  "#f2b603","#f2b603"))
                    mid.append(imprimir_color('   ', "#f2b603","#f2b603"))
                else:
                    mid.append(imprimir_color('║',"#29a93e") if (cell & 8 or (j > 0 and maze[i][j-1] & 2)) else ' ')
                    mid.append('   ')
            mid.append(imprimir_color('║',"#29a93e") if (maze[i][cols-1] & 2) else ' ')
            screen.append(mid)
            
        bottom = []
        for j in range(cols):
            cell = maze[i][j]
            if cell == 15:
                bottom.append(imprimir_color('¤', "#29a93e","#29a93e"))
                bottom.append(imprimir_color('═══',  "#29a93e","#29a93e"))
            else:
                bottom.append(imprimir_color('¤',"#bef14b"))
                bottom.append(imprimir_color('═══',"#29a93e") if (cell & 4 or (i+1 < rows and maze[i+1][j] & 1)) else '   ')
        bottom.append(imprimir_color('¤',"#bef14b"))
        screen.append(bottom)

        full_width = cols * 4 + 1
        for row in screen:
            while len(row) < full_width:
                row.append(' ')

        row_idx = entry[0]*2 + 1
        col_idx = entry[1]*2 + 1  
        screen[col_idx][row_idx] = imprimir_color(' O ', "#FFFFFF", "#0026FF")

        row_idx = exit[0]*2 + 1
        col_idx = exit[1]*2 + 1
        screen[col_idx][row_idx] = imprimir_color(' X ', "#ffffff","#c91f1f")


        for line in screen:
            print("".join(line))

        print(f"\n---\nFile '{sys.argv[1]}' closed")

    except PermissionError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
    except FileNotFoundError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
 


from colorama import Style

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
    create_lab()