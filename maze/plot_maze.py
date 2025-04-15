from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

def plot_maze(L):
    n = len(L)       # rows
    m = len(L[0])    # columns

    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Expand plot area by 0.5 in each direction
    ax.set_xlim(-0.1, m + 0.1)
    ax.set_ylim(-0.1, n + 0.1)

    ax.set_xticks(range(m + 1))
    ax.set_yticks(range(n + 1))
    ax.grid(True, color='gray', linewidth=1)

    ax.invert_yaxis()  # So that L[0][0] is at top-left
    ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

    # Remove outer frame box
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Fill fully enclosed cells



    for i in range(n):
        for j in range(m):
            if L[i][j] != 15:
                x0 = j
                y0 = i
                rect = Rectangle((x0, y0), 1, 1, facecolor='#dddddd', edgecolor='none', zorder=0)
                ax.add_patch(rect)

    # Draw walls
    for i in range(n):
        for j in range(m):
            x0 = j
            y0 = i

            if L[i][j] & 2:  # top
                ax.plot([x0 + 0.1, x0 + 0.9], [y0, y0], color='#008877', linewidth=3.5)
            if L[i][j] & 1:  # bottom
                ax.plot([x0 + 0.1, x0 + 0.9], [y0 + 1, y0 + 1], color='#008877', linewidth=3.5)
            if L[i][j] & 8:  # left
                ax.plot([x0, x0], [y0 + 0.1, y0 + 0.9], color='#008877', linewidth=3.5)
            if L[i][j] & 4:  # right
                ax.plot([x0 + 1, x0 + 1], [y0 + 0.1, y0 + 0.9], color='#008877', linewidth=3.5)

    plt.show()
