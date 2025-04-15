"""
`ascii_to_L.py` generates an maze L given a drawn maze in ascii-style in a `.txt`-file.
	- 3 dashes `---` represent a horizontal wall
	- 3 empty spaces `␣␣␣` represents the absence of a horizontal wall
	- `|` represents a vertical wall
	- `+`represents the corner of a cell
	- Important: You cant use tabs, use blank space characters!
"""


def ascii_to_L(filename):
    """
    Reads an ASCII maze from a file and converts it to matrix L using wall encoding:
    Encoding uses:
        Bit 0: +x (bottom)
        Bit 1: -x (top)
        Bit 2: +y (right)
        Bit 3: -y (left)
    Each cell is 2x2 characters surrounded by walls, so the full grid:
        rows = 2*n + 1
        cols = 4*m + 1
    """
    with open(filename, 'r') as f:
        ascii_lines = [line.rstrip('\n') for line in f]

    rows = len(ascii_lines)
    cols = len(ascii_lines[0])
    n = (rows - 1) // 2
    m = (cols - 1) // 4

    L = [[0 for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            code = 0
            top_wall = ascii_lines[2 * i][4 * j + 1:4 * j + 4]
            bottom_wall = ascii_lines[2 * i + 2][4 * j + 1:4 * j + 4]
            left_wall = ascii_lines[2 * i + 1][4 * j]
            right_wall = ascii_lines[2 * i + 1][4 * j + 4]

            if top_wall == '---':
                code |= 2  # -x
            if bottom_wall == '---':
                code |= 1  # +x
            if right_wall == '|':
                code |= 4  # +y
            if left_wall == '|':
                code |= 8  # -y

            L[i][j] = code

    return L
