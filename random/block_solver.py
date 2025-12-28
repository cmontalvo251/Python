# Import modules
import numpy as np
import matplotlib.pyplot as plt
import time

# Global flag for video output
VIDEOFLAG = False # Set to True to see step-by-step placement, False for instant solution
DEBUGFLAG = False
iteration_count = 0

# ## Implement Block Operations
# Create helper functions for block manipulation and placement.
def normalize_block_shape(block_shape):
    """
    Normalizes a block shape by shifting all coordinates so the top-most, left-most point is (0,0).
    """
    if not block_shape: # Handle empty block shape
        return []
    min_r = min(p[0] for p in block_shape)
    min_c = min(p[1] for p in block_shape)
    normalized = sorted([(p[0] - min_r, p[1] - min_c) for p in block_shape])
    return normalized

def flip_block_horizontal(block_shape):
    """
    Flips a block shape horizontally.
    """
    if not block_shape:
        return []
    # Find the maximum column value within the block's current coordinates
    # This ensures the flip is relative to the block's own width.
    max_c_val = max(p[1] for p in block_shape)
    flipped_shape = [(r, max_c_val - c) for r, c in block_shape]
    return flipped_shape

def rotate_block(block_shape):
    """
    Takes a block shape (list of relative coordinates) and returns a list of all unique
    90-degree rotated orientations of that block, including flipped versions.
    """
    all_orientations = set()

    # Process original orientations
    current_shape = block_shape
    for _ in range(4):
        all_orientations.add(tuple(normalize_block_shape(current_shape)))
        # Rotate 90 degrees clockwise: (r, c) -> (c, -r)
        current_shape = [(c, -r) for r, c in current_shape]

    # Process flipped orientations
    # Flip the original block once, then generate its rotations
    flipped_initial_shape = flip_block_horizontal(block_shape)
    current_shape = flipped_initial_shape
    for _ in range(4):
        all_orientations.add(tuple(normalize_block_shape(current_shape)))
        # Rotate 90 degrees clockwise: (r, c) -> (c, -r)
        current_shape = [(c, -r) for r, c in current_shape]

    return [list(o) for o in all_orientations]

def find_first_empty_cell(grid):
    """
    Iterates through the grid (row by row, then column by column) and returns the
    (row, col) coordinates of the first cell with a value of 0. If no empty cell
    is found, return None.
    """
    grid_rows = len(grid)
    grid_cols = len(grid[0]) if grid_rows > 0 else 0

    for r in range(grid_rows):
        for c in range(grid_cols):
            if grid[r][c] == 0:
                return (r, c)
    return None

def check_fit(grid, block_shape, start_row, start_col):
    """
    Checks if a block_shape can be placed at (start_row, start_col) in the grid.
    Returns True if the block fits without going out of bounds and without overlapping.
    """
    grid_rows = len(grid)
    grid_cols = len(grid[0])

    for dr, dc in block_shape:
        r, c = start_row + dr, start_col + dc

        # Check bounds
        if not (0 <= r < grid_rows and 0 <= c < grid_cols):
            return False

        # Check for overlap with occupied cells
        if grid[r][c] != 0:
            return False

    return True

def place_block(grid, block_shape, start_row, start_col, block_id):
    """
    Attempts to place a block_shape at (start_row, start_col) in a copy of the grid.
    If the block fits, it returns the modified grid with the block's cells marked by block_id.
    If the block does not fit, or if any placement is invalid, return None.
    """
    if VIDEOFLAG:
        temp_grid = [row[:] for row in grid]
        grid_rows = len(grid)
        grid_cols = len(grid[0])
        for dr, dc in block_shape:
            r, c = start_row + dr, start_col + dc
            if 0 <= r < grid_rows and 0 <= c < grid_cols:
                temp_grid[r][c] = block_id
        plot_grid(temp_grid, block_colors, block_id)

    if not check_fit(grid, block_shape, start_row, start_col):
        if DEBUGFLAG:
            print(f"  Block {block_id} (orientation {block_shape}) does NOT fit at ({start_row}, {start_col})")
        return None

    new_grid = [row[:] for row in grid] # Create a deep copy of the grid

    for dr, dc in block_shape:
        r, c = start_row + dr, start_col + dc
        new_grid[r][c] = block_id

    if DEBUGFLAG:
        print(f"  Block {block_id} (orientation {block_shape}) placed at ({start_row}, {start_col})")
        for row in new_grid:
            print(f"    {row}")
    return new_grid

def plot_grid(grid, block_colors_map, current_block_id=None, force=False):
    """
    Plots the current state of the grid with colored blocks.
    """
    if not VIDEOFLAG and not force:  # Only plot if visualization is on
        return

    grid_rows = len(grid)
    grid_cols = len(grid[0])

    # Create a color mapping from block_id to color string
    color_map = {0: 'white', -1: 'gray'}  # 0 is empty, -1 is dead zone
    color_map.update(block_colors_map)

    plt.clf()
    ax = plt.gca()
    ax.set_xlim(-0.5, grid_cols - 0.5)
    ax.set_ylim(grid_rows - 0.5, -0.5)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks(np.arange(grid_cols))
    ax.set_yticks(np.arange(grid_rows))
    ax.tick_params(axis='both', which='both', length=0)
    ax.grid(False)  # We draw our own grid/edges

    # Draw each cell as a rectangle with an edge
    for r in range(grid_rows):
        for c in range(grid_cols):
            block_id = int(grid[r][c])
            color = color_map.get(block_id, 'lightgray')  # Default to gray if id not in map

            # For blocks, use a black edge. For empty cells, a light gray one.
            edge_color = 'black' if block_id != 0 else 'lightgray'

            rect = plt.Rectangle((c - 0.5, r - 0.5), 1, 1,
                                 facecolor=color,
                                 edgecolor=edge_color,
                                 linewidth=1)
            ax.add_patch(rect)

            if block_id != 0 and block_id != -1:
                # Determine text color for contrast. A simple luminance check.
                from matplotlib.colors import to_rgb
                rgb = to_rgb(color)
                luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
                text_color = 'white' if luminance < 0.5 else 'black'
                plt.text(c, r, str(block_id), ha='center', va='center', color=text_color, fontsize=12)

    plt.title(f"Block Placement - Current ID: {current_block_id if current_block_id is not None else 'Final'}")
    plt.draw()
    plt.pause(0.01)  # Pause for x seconds to show the frame

# ## Develop Recursive Solver
# Implement a recursive function solve(current_grid, blocks_to_place, current_block_id) to find a solution for placing the blocks.
def solve(current_grid, blocks_to_place):
    """
    Recursively attempts to place blocks on the grid to find a solution.
    """
    global iteration_count
    # Base case: If all blocks are placed, return the current grid as a solution.
    if not blocks_to_place:
        return current_grid

    grid_rows = len(current_grid)
    grid_cols = len(current_grid[0])

    # If there are no empty cells left, check if we have placed all blocks.
    if not find_first_empty_cell(current_grid):
        # If we are here, grid is full, but blocks_to_place is not empty. This is a failed path.
        if DEBUGFLAG:
            print("Grid is full, but blocks remain. Backtracking.")
        return None

    # Iterate through all available blocks to choose which one to place next.
    for i in range(len(blocks_to_place)):
        block_id, block_shape = blocks_to_place[i]
        remaining_blocks = blocks_to_place[:i] + blocks_to_place[i+1:]

        if DEBUGFLAG:
            print(f"\n---\nPicking block {block_id} to place next.")

        # Generate all unique orientations for this block (including flips)
        orientations = rotate_block(block_shape)

        # Try placing this block at every possible start coordinate (r, c).
        # This is a less efficient search strategy than filling the 'first empty cell'
        # because it will try the same set of placements in different orders (permutations).
        # However, it directly addresses the concern about being 'restricted' to one cell.
        for r_start in range(grid_rows):
            for c_start in range(grid_cols):
                # Optimization: Only try to start a placement on an empty cell.
                # Since all block shapes are normalized to include a (0,0) point,
                # attempting to place a block on an already occupied cell will always fail.
                # This check avoids calling place_block unnecessarily for invalid starting points.
                if current_grid[r_start][c_start] == 0:
                    for orientation in orientations:
                        iteration_count += 1
                        print(f"Iteration number = {iteration_count}")
                        # place_block will check for fit and return a new grid or None
                        new_grid_after_placement = place_block(current_grid, orientation, r_start, c_start, block_id)

                        if new_grid_after_placement is not None:
                            # If placement was successful, recurse
                            result = solve(new_grid_after_placement, remaining_blocks)
                            if result is not None:
                                return result

    # If we've tried placing every available block everywhere and found no path, backtrack.
    if DEBUGFLAG:
        print("Could not find a valid placement for any remaining block. Backtracking.")
    return None

# Task: Solve an NxN grid puzzle by placing blocks
starting_time = time.time()

# ## Define Grid and Blocks
# Initialize an NxN occupancy grid filled with zeros
#grid_size = (6, 4) #Level 4
#grid_size = (4,3) #Level 1
#grid_size = (5, 4) #Level 3
grid_size = (6, 4) #Level 2
grid = np.zeros(grid_size, dtype=int).tolist() # Convert numpy array to list for easier manipulation

#Add Dead zones in the corners
grid[0][0] = -1
grid[5][0] = -1
grid[0][3] = -1
grid[5][3] = -1

# Define the shape of the 3x2 block as a list of relative coordinates
block_L = [
    (0, 0),
    (1, 0),
    (2, 0), (2, 1)
]

block_S = [
    (0, 0), (0, 1),
    (1, 0), (1, 1)
]

# Define the shape of the 3x1 block as a list of relative coordinates
block_T = [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 1)
]

block_I = [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3)
]

block_Z = [
    (0, 0), (0, 1),
            (1, 1), (1, 2)
]

# Define block colors
block_colors = {
    1: 'red',
    2: 'red',
    3: 'yellow',
    4: 'green',
    5: 'green',
}

"""
block_colors = {
    1: 'orange',
    2: 'yellow',
    3: 'blue',
    4: 'blue',
    5: 'blue',
}
"""
"""
block_colors = {
    1: 'red', # block_Z
    2: 'blue', # block_I (first instance)
    3: 'blue',  # block_I (second instance)
    4: 'blue',  # block_L
    5: 'purple', # block_T
    6: 'purple' # block_T
}
block_colors = {
    1: 'blue',
    2: 'purple',
    3: 'purple',
}
"""
# ## Execute and Display Solution
# Call the solve function with the initial NxN grid, a list of the two blocks, and the starting block ID (e.g., 1). Print the resulting grid if a solution is found, otherwise indicate that no solution exists.
blocks_to_place = [
    (1, block_Z),
    (2, block_Z),
    (3, block_S),
    (4, block_Z),
    (5, block_Z),
]
"""
blocks_to_place = [
    (1, block_L),
    (2, block_S),
    (3, block_I),
    (4, block_I),
    (5, block_L),
]
"""
"""
blocks_to_place = [
    (1, block_Z),
    (2, block_I),
    (3, block_I),
    (4, block_L),
    (5, block_T),
    (6, block_T)
]
blocks_to_place = [
    (1, block_L),
    (2, block_T),
    (3, block_T)
]
"""

solution = solve(grid, blocks_to_place)

end_time = time.time()
print(f"\nTotal solving time: {end_time - starting_time:.4f} seconds\n")

if solution is not None:
    print("Solution Found:")
    for row in solution:
        print(row)
    #plot final solution
    plot_grid(solution, block_colors, force=True)
    plt.show() # Keep the final plot open
else:
    print("No solution found for the puzzle.")
