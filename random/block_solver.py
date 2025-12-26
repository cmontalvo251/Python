# Import modules
import numpy as np
import matplotlib.pyplot as plt
import time

# Global flag for video output
VIDEOFLAG = True # Set to True to see step-by-step placement, False for instant solution

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
    if not check_fit(grid, block_shape, start_row, start_col):
        print(f"  Block {block_id} (orientation {block_shape}) does NOT fit at ({start_row}, {start_col})")
        return None

    new_grid = [row[:] for row in grid] # Create a deep copy of the grid

    for dr, dc in block_shape:
        r, c = start_row + dr, start_col + dc
        new_grid[r][c] = block_id

    print(f"  Block {block_id} (orientation {block_shape}) placed at ({start_row}, {start_col})")
    for row in new_grid:
        print(f"    {row}")
    if VIDEOFLAG:
        plot_grid(new_grid, block_colors, block_id)
    return new_grid

def plot_grid(grid, block_colors_map, current_block_id=None):
    """
    Plots the current state of the grid with colored blocks.
    """
    if not VIDEOFLAG: # Only plot if visualization is on
        return

    # Create a colormap. 0 for empty, then map block_ids to colors
    # Ensure the colormap has enough distinct colors
    max_id = max(block_colors_map.keys()) if block_colors_map else 0
    colors = ['lightgray'] * (max_id + 1)
    for block_id, color in block_colors_map.items():
        colors[block_id] = color
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(colors)

    plt.clf()
    plt.imshow(grid, cmap=cmap, origin='upper', extent=[-0.5, len(grid[0])-0.5, len(grid)-0.5, -0.5], vmin=0, vmax=max_id) # Adjust extent for cell-centered display
    plt.grid(True, color='black', linewidth=1)
    plt.xticks(np.arange(len(grid[0])))
    plt.yticks(np.arange(len(grid)))
    plt.tick_params(axis='both', which='both', length=0) # Hide ticks

    # Add labels for blocks
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != 0:
                plt.text(c, r, str(int(grid[r][c])), ha='center', va='center', color='black', fontsize=12)

    plt.title(f"Block Placement - Current ID: {current_block_id if current_block_id is not None else 'Final'}")
    plt.draw()
    plt.pause(1.0) # Pause for 0.1 seconds to show the frame

# ## Develop Recursive Solver
# Implement a recursive function solve(current_grid, blocks_to_place, current_block_id) to find a solution for placing the blocks.
def solve(current_grid, blocks_to_place, current_block_id):
    """
    Recursively attempts to place blocks on the grid to find a solution.
    """
    # Base case: If all blocks are placed, return the current grid as a solution.
    if not blocks_to_place:
        return current_grid

    # Find the first empty cell in the current grid
    first_empty = find_first_empty_cell(current_grid)

    # If no empty cell is found but there are still blocks to place, this path is invalid.
    # This shouldn't happen if the grid is filled correctly, but serves as a safeguard.
    if first_empty is None and blocks_to_place:
        print(f"No empty cell found, but blocks to place. Backtracking from ID: {current_block_id}")
        return None

    first_empty_r, first_empty_c = first_empty

    # Take the first block from the list of blocks to place
    block_to_place = blocks_to_place[0]
    remaining_blocks = blocks_to_place[1:]

    print(f"\nTrying to place block ID {current_block_id} at first empty cell ({first_empty_r}, {first_empty_c})")
    print(f"Current Grid (before trying block {current_block_id}):")
    for row in current_grid:
        print(f"  {row}")

    # Generate all unique orientations for this block (including flips)
    orientations = rotate_block(block_to_place)

    # Try placing each orientation of the block
    for orientation in orientations:
        # For each point (dr, dc) in the current orientation, try aligning it with first_empty_r, first_empty_c
        for dr_anchor, dc_anchor in orientation:
            potential_start_row = first_empty_r - dr_anchor
            potential_start_col = first_empty_c - dc_anchor

            # Attempt to place the orientation at the calculated start_row, start_col
            # The place_block function checks for fit and returns a new grid or None
            new_grid_after_placement = place_block(current_grid, orientation, potential_start_row, potential_start_col, current_block_id)

            if new_grid_after_placement is not None:
                print(f"Successfully placed block {current_block_id}. New grid:")
                for row in new_grid_after_placement:
                    print(f"  {row}")
                # If placement was successful, recursively call solve for the next block
                result = solve(new_grid_after_placement, remaining_blocks, current_block_id + 1)
                if result is not None:
                    # If a solution is found in the recursive call, propagate it up
                    return result
    print(f"No valid placement found for block ID {current_block_id} at ({first_empty_r}, {first_empty_c}). Backtracking.")
    # If no orientation or subsequent recursive call leads to a solution, backtrack
    return None

# Task: Solve an NxN grid puzzle by placing blocks

# ## Define Grid and Blocks
# Initialize an NxN occupancy grid filled with zeros
grid_size = (6, 4)
grid = np.zeros(grid_size, dtype=int).tolist() # Convert numpy array to list for easier manipulation

# Define the shape of the 3x2 block as a list of relative coordinates
block_L = [
    (0, 0),
    (1, 0),
    (2, 0), (2, 1)
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
    1: 'red', # block_Z
    2: 'blue', # block_I (first instance)
    3: 'blue',  # block_I (second instance)
    4: 'blue',  # block_L
    5: 'purple', # block_T
    6: 'purple' # block_T
}

# ## Execute and Display Solution
# Call the solve function with the initial NxN grid, a list of the two blocks, and the starting block ID (e.g., 1). Print the resulting grid if a solution is found, otherwise indicate that no solution exists.
blocks_to_place = [block_Z,block_I,block_I,block_L,block_T,block_T]
starting_block_id = 1

solution = solve(grid, blocks_to_place, starting_block_id)

if solution is not None:
    print("Solution Found:")
    for row in solution:
        print(row)
    if VIDEOFLAG: # Display final solution if visualization is on
        plot_grid(solution, block_colors)
        plt.show() # Keep the final plot open
else:
    print("No solution found for the puzzle.")
