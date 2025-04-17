import random

# generates a random maze, given a size and filling factor.
# this maze starts on the top-left (0,0) and is always > 1 cell
# however, it is not guaranteed that the maze is fully connected or valid!

def generate_random_maze(*size, filling_factor=50):
    # --- Determine maze size ---
    if len(size) == 0:
        n = random.randint(2, 20)
        m = random.randint(2, 20)
    elif len(size) == 1:
        n = m = max(2, size[0])
    elif len(size) == 2:
        n = max(2, size[0])
        m = max(2, size[1])
    else:
        raise ValueError("At most two dimensions allowed")

    # --- Initialize maze with outer walls ---
    L = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            val = 0
            if i == 0: val |= 2
            if i == n - 1: val |= 1
            if j == 0: val |= 8
            if j == m - 1: val |= 4
            L[i][j] = val

    # --- Random inner walls ---
    total_possible_inner_walls = (n - 1) * m + (m - 1) * n
    num_inner_walls = int((filling_factor / 100) * total_possible_inner_walls)

    wall_candidates = []
    for i in range(n - 1):
        for j in range(m):
            wall_candidates.append(("H", i, j))  # (i,j) and (i+1,j)
    for i in range(n):
        for j in range(m - 1):
            wall_candidates.append(("V", i, j))  # (i,j) and (i,j+1)

    chosen_walls = random.sample(wall_candidates, num_inner_walls)
    for wall_type, i, j in chosen_walls:
        if wall_type == "H":
            L[i][j] |= 1
            L[i + 1][j] |= 2
        elif wall_type == "V":
            L[i][j] |= 4
            L[i][j + 1] |= 8

    # --- Ensure (0,0) is not fully enclosed ---
    if L[0][0] == 15:
        removable = []
        if not (L[0][0] & 1) and n > 1: removable.append(1)  # bottom
        if not (L[0][0] & 4) and m > 1: removable.append(4)  # right

        if removable:
            wall = random.choice(removable)
            if wall == 1:
                L[0][0] &= ~1
                L[1][0] &= ~2
            elif wall == 4:
                L[0][0] &= ~4
                L[0][1] &= ~8
        else:
            L[0][0] &= ~1
            L[1][0] &= ~2

    return L
