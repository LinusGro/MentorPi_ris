def draw_ascii_maze(L):
    n = len(L)
    m = len(L[0])
    lines = []

    for i in range(n):
        top_line = "+"
        for j in range(m):
            top_line += "---+" if L[i][j] & 2 else "   +"
        lines.append(top_line)

        mid_line = ""
        for j in range(m):
            mid_line += "|" if L[i][j] & 8 else " "
            mid_line += "   "
        mid_line += "|" if L[i][m - 1] & 4 else " "
        lines.append(mid_line)

    bottom_line = "+"
    for j in range(m):
        bottom_line += "---+" if L[n - 1][j] & 1 else "   +"
    lines.append(bottom_line)

    for line in lines:
        print(line)
