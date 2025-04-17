"""
- `validate_maze.py`checks if a maze L is valid
	- all entries in L are in `[0,...,15]`
	- if a wall exists on one cell, it must exist on the neighboring cell
	- all nonreachable cells are marked with `(1111)`
	- all outer walls exist
	- checks, if the maze is minimum size or if it can be trimmed, ie if all cells in an outer row/column are non-reachable
"""


def validate_maze(L):
    if not L:
        raise ValueError("Maze is empty")

    n = len(L)
    m = len(L[0])

    # --- Check rectangularity and range ---
    for i, row in enumerate(L):
        if len(row) != m:
            raise ValueError(f"Row {i} does not match expected column size {m}")
        for j, value in enumerate(row):
            if not (0 <= value <= 15):
                raise ValueError(f"Invalid entry L[{i}][{j}] = {value}, must be in [0, 15]")

    # --- Check wall consistency between adjacent cells ---
    for i in range(n):
        for j in range(m):
            cell = L[i][j]
            if i < n - 1:
                below = L[i + 1][j]
                if ((cell & 1) >> 0) != ((below & 2) >> 1):
                    raise ValueError(f"Inconsistent wall between ({i+1},{j+1}) and ({i + 1+1},{j+1})")
            if j < m - 1:
                right = L[i][j + 1]
                if ((cell & 4) >> 2) != ((right & 8) >> 3):
                    raise ValueError(f"Inconsistent wall between ({i+1},{j+1}) and ({i+1},{j + 1+1})")

    # --- Check outer boundary walls ---
    for j in range(m):
        if not (L[0][j] & 2):
            raise ValueError(f"Missing top wall at (1,{j+1})")
        if not (L[n - 1][j] & 1):
            raise ValueError(f"Missing bottom wall at ({n - 1+1},{j+1})")
    for i in range(n):
        if not (L[i][0] & 8):
            raise ValueError(f"Missing left wall at ({i+1},1)")
        if not (L[i][m - 1] & 4):
            raise ValueError(f"Missing right wall at ({i+1},{m - 1+1})")

    # --- Check unreachable cells and trimming possibility ---
    from collections import deque

    visited = [[False for _ in range(m)] for _ in range(n)]

    # BFS or DFS from (0,0) to mark reachable cells
    def dfs(i, j):
        stack = deque()
        stack.append((i, j))
        while stack:
            x, y = stack.pop()
            if visited[x][y]:
                continue
            visited[x][y] = True
            cell = L[x][y]
            if x > 0 and not (cell & 2) and not visited[x - 1][y]:
                stack.append((x - 1, y))
            if x < n - 1 and not (cell & 1) and not visited[x + 1][y]:
                stack.append((x + 1, y))
            if y > 0 and not (cell & 8) and not visited[x][y - 1]:
                stack.append((x, y - 1))
            if y < m - 1 and not (cell & 4) and not visited[x][y + 1]:
                stack.append((x, y + 1))

    dfs(0, 0)

    # Check for incorrectly marked unreachable cells
    unreachable_errors = []
    for i in range(n):
        for j in range(m):
            if not visited[i][j] and L[i][j] != 15:
                unreachable_errors.append((i, j))

    if unreachable_errors:
        print("Unreachable cells not marked with 15:")
        for i, j in unreachable_errors:
            print(f" - L[{i}][{j}] = {L[i][j]} (should be 15)")

    # Check if any outer rows or columns can be trimmed
    def row_all_15(row):
        return all(cell == 15 for cell in row)

    def col_all_15(col_idx):
        return all(L[i][col_idx] == 15 for i in range(n))

    trimmable = False
    if row_all_15(L[0]):
        print("Top row can be trimmed (all 15).")
        trimmable = True
    if row_all_15(L[-1]):
        print("Bottom row can be trimmed (all 15).")
        trimmable = True
    if col_all_15(0):
        print("Left column can be trimmed (all 15).")
        trimmable = True
    if col_all_15(m - 1):
        print("Right column can be trimmed (all 15).")
        trimmable = True

    # Final output
    if not unreachable_errors and not trimmable:
        print("Maze is valid.")
