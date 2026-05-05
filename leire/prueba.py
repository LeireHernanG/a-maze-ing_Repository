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

            rows = len(maze)
            cols = len(maze[0])
            entry = [int(x) for x in archivo.readline().strip().split(",")]
            exit = [int(x) for x in archivo.readline().strip().split(",")]
            solution = archivo.readline().strip()

        screen = []

        for i in range(rows):
            top = []
            mid = []
            for j in range(cols):
                cell = maze[i][j]
                top.append('+')
                top.append('---' if cell & 1 else '   ')
                mid.append('|' if cell & 8 else ' ')
                mid.append('   ')
            top.append('+')
            mid.append('|' if maze[i][-1] & 2 else ' ')
            screen.append(top)
            screen.append(mid)

        bottom = []
        for j in range(cols):
            bottom.append('+')
            bottom.append('---' if maze[-1][j] & 4 else '   ')
        bottom.append('+')
        screen.append(bottom)

        full_width = cols * 4 + 1
        for row in screen:
            while len(row) < full_width:
                row.append(' ')

        row_idx = entry[0]*2 + 1
        col_idx = entry[1]*4 + 2
        screen[row_idx][col_idx] = 'O'

        row_idx = exit[0]*2 + 1
        col_idx = exit[1]*4 + 2
        screen[row_idx][col_idx] = 'X'

        for line in screen:
            print("".join(line))

        print(f"\n---\nFile '{sys.argv[1]}' closed")

    except PermissionError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
    except FileNotFoundError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
 



if __name__ == "__main__":
    create_lab()




""" def create_lab() -> None:
    import sys

    maze = []
    if len(sys.argv) == 1:
        print("Usage: visual.py <file>")
        return

    try:
        with open(sys.argv[1], 'r') as archivo:
            first_line = archivo.readline().strip()
            first_row = [int(x, 16) for x in first_line.split()]
            expected_cols = len(first_row)
            maze.append(first_row)

            for line in archivo:
                line = line.strip()
                if not line:
                    break
                row = [int(x, 16) for x in line.split()]
                if len(row) != expected_cols:
                    raise ValueError(f"Row has wrong length {len(row)}, expected {expected_cols}")
                maze.append(row)

            entry = [int(x) for x in archivo.readline().strip().split(",")]
            exit = [int(x) for x in archivo.readline().strip().split(",")]
            solution = archivo.readline().strip().split()

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
                mid.append('|' if cell & 2 else ' ')
                
            top.append('+')
            screen.append(top)
            screen.append(mid)

        bottom = []
        for cell in maze[-1]:
            bottom.append('+')
            bottom.append('---' if cell & 4 else '   ')
        bottom.append('+')
        screen.append(bottom)

        screen[exit[0]*2 + 1][exit[1]*4 + 2] = 'X'
        screen[entry[0]*2 + 1][entry[1]*4 + 2] = 'O'

        for line in screen:
            print("".join(line))

        print(f"\n---\nFile '{sys.argv[1]}' closed")

    except PermissionError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")
    except FileNotFoundError as e:
        print(f"Error opening file '{sys.argv[1]}': {e}")

        
  """