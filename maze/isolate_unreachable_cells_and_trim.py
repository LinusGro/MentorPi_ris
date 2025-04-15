"""
- `isolate_unreachable_cells_and_trim.py`marks unreachable cells in the maze with `(1111)` and trims the maze, if all outer cells in a row/column are non-reachable
"""


def isolate_unreachable_cells_and_trim(L):
    def mark_unreachable(L):
        n = len(L)
        m = len(L[0])
        visited = [[False for _ in range(m)] for _ in range(n)]

        def dfs(i, j):
            if visited[i][j]:
                return
            visited[i][j] = True
            cell = L[i][j]
            if i > 0 and not (cell & 2): dfs(i - 1, j)
            if i < n - 1 and not (cell & 1): dfs(i + 1, j)
            if j > 0 and not (cell & 8): dfs(i, j - 1)
            if j < m - 1 and not (cell & 4): dfs(i, j + 1)

        dfs(0, 0)

        for i in range(n):
            for j in range(m):
                if not visited[i][j]:
                    val = 15
                    if i == 0: val |= 2
                    if i == n - 1: val |= 1
                    if j == 0: val |= 8
                    if j == m - 1: val |= 4
                    L[i][j] = val
        return L

    def trim_unreachable_edges(L):
        changed = False
        n = len(L)
        m = len(L[0]) if n > 0 else 0

        while n > 0 and all(cell == 15 for cell in L[0]):
            L = L[1:]
            changed = True
            n -= 1
        while n > 0 and all(cell == 15 for cell in L[-1]):
            L = L[:-1]
            changed = True
            n -= 1
        if n == 0:
            return L, changed

        m = len(L[0])
        while m > 0 and all(row[0] == 15 for row in L):
            L = [row[1:] for row in L]
            changed = True
            m -= 1
        while m > 0 and all(row[-1] == 15 for row in L):
            L = [row[:-1] for row in L]
            changed = True
            m -= 1

        return L, changed

    L = mark_unreachable(L)
    while True:
        L, changed = trim_unreachable_edges(L)
        if not changed:
            break
    return L
