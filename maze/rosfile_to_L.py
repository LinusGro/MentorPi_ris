def load_maze_from_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if len(lines) < 5:
        raise ValueError("File too short to contain valid maze information.")

    n = int(lines[0])
    m = int(lines[1])

    expected_elements = n * m
    actual_elements = len(lines) - 5
    if actual_elements != expected_elements:
        raise ValueError(f"Expected {expected_elements} maze elements, but found {actual_elements}.")

    flat_L = list(map(int, lines[5:]))
    L = [flat_L[i * m:(i + 1) * m] for i in range(n)]

    return L
