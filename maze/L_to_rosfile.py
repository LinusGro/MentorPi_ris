def save_maze_to_file(L, filename):
    n = len(L)
    m = len(L[0])


    # --- Ask user for start_idx, end_idx, and start_orientation ---
    start_idx = input("Enter start index: ")
    end_idx = input("Enter end index: ")
    start_orientation = input("Enter start orientation: ")

    try:
        start_idx = int(start_idx)
        end_idx = int(end_idx)
        start_orientation = int(start_orientation)
    except ValueError:
        print("Error: Inputs must be integers.")
        return

    # --- Flatten the maze ---
    flat_L = [cell for row in L for cell in row]

    # --- Write to file ---
    with open(filename, 'w') as f:
        f.write(f"{n}\n")
        f.write(f"{m}\n")
        f.write(f"{start_idx}\n")
        f.write(f"{end_idx}\n")
        f.write(f"{start_orientation}\n")
        for value in flat_L:
            f.write(f"{value}\n")

    print(f"Maze successfully saved to '{filename}'.")


