from ascii_to_L import ascii_to_L
from draw_ascii_maze import draw_ascii_maze
from isolate_unreachable_cells_and_trim import isolate_unreachable_cells_and_trim
from validate_maze import validate_maze
from generate_random_maze import generate_random_maze
from plot_maze import plot_maze

if __name__ == "__main__":
    # Generate a random maze with filling factor
    L_random = generate_random_maze(15, 6, filling_factor=15)
    # type your own maze
    L_example = [[10, 2, 2, 2, 2, 6],
                 [8, 0, 1, 1, 0, 4],
                 [8, 4, 10, 2, 0, 4],
                 [8, 4, 9, 1, 0, 4],
                 [8, 0, 2, 2, 0, 4],
                 [9, 1, 1, 1, 1, 5]]
    # or draw it ascii-style in the txt.-file
    L_ascii = ascii_to_L("ascii_maze.txt")

    # choose L
    L = L_ascii

    #validate maze - could still be invalid if it is drawn or generated randomly
    validate_maze(L)
    #mark unreachable cells and trim the maze
    L = isolate_unreachable_cells_and_trim(L)

    #validate maze - now it has to be valid
    validate_maze(L)

    # Output ASCII version
    print("ASCII Representation of Maze:")
    draw_ascii_maze(L)

    # Plot the maze
    print("Plotting Maze...")
    plot_maze(L)
