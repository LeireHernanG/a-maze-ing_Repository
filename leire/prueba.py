def create_lab() -> None:
    import sys

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
            print(maze)
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
                top.append('+')
                top.append('---' if (cell & 1 or (i > 0 and maze[i-1][j] & 4)) else '   ')
            top.append('+')
            screen.append(top)
            
            mid = []
            for j in range(cols):
                cell = maze[i][j]
                mid.append('|' if (cell & 8 or (j > 0 and maze[i][j-1] & 2)) else ' ')
                mid.append('   ')
            mid.append('|' if (maze[i][cols-1] & 2) else ' ')
            screen.append(mid)
            
        bottom = []
        for j in range(cols):
            cell = maze[i][j]
            bottom.append('+')
            bottom.append('---' if (cell & 4 or (i+1 < rows and maze[i+1][j] & 1)) else '   ')
        bottom.append('+')
        screen.append(bottom)

        full_width = cols * 4 + 1
        for row in screen:
            while len(row) < full_width:
                row.append(' ')

        row_idx = entry[0]*2 + 0
        col_idx = entry[1]*2 + 1  
        screen[row_idx][col_idx] = ' O ' 

        row_idx = exit[0]*2 + 1
        col_idx = exit[1]*2 + 1
        screen[row_idx][col_idx] = ' X '


        for line in screen:
            print("".join(line))

        print(f"\n---\nFile '{sys.argv[1]}' closed")

    except PermissionError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
    except FileNotFoundError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
 



if __name__ == "__main__":
    create_lab()
