# Import modules
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# Global flag for video output
VIDEOFLAG = False # Set to True to see step-by-step placement, False for instant solution
DEBUGFLAG = False
BLOCKFLAG = True #Turn on to view blocks
MOBILEFLAG = False
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
def solve(initial_grid, blocks_to_place):
    """
    Iterative solver using random permutations and greedy placement.
    Loops until a solution is found.
    """
    global iteration_count
    iteration_count = 0
    
    # Pre-calculate orientations for all blocks
    blocks_data = []
    for b_id, b_shape in blocks_to_place:
        orientations = rotate_block(b_shape)
        blocks_data.append((b_id, orientations))
    
    print("Starting iterative solver...")
    
    while True:
        iteration_count += 1
        if iteration_count % 1000 == 0:
            print(f"Iteration {iteration_count}...")
            
        # Shuffle the order of blocks
        random.shuffle(blocks_data)
        
        # Create a working copy of the grid
        current_grid = [row[:] for row in initial_grid]
        
        all_placed = True
        
        for b_id, orientations in blocks_data:
            # Find the first empty cell that needs covering
            target = find_first_empty_cell(current_grid)
            
            if target is None:
                # Grid is full but we still have blocks to place
                all_placed = False
                break
            
            target_r, target_c = target
            placed_this_block = False
            
            # Try orientations in random order
            current_orientations = random.sample(orientations, len(orientations))
            
            for orientation in current_orientations:
                # Try to anchor different cells of the block to the target cell
                anchor_indices = list(range(len(orientation)))
                random.shuffle(anchor_indices)
                
                for idx in anchor_indices:
                    dr_anchor, dc_anchor = orientation[idx]
                    
                    # Calculate top-left position of the block
                    start_r = target_r - dr_anchor
                    start_c = target_c - dc_anchor
                    
                    if check_fit(current_grid, orientation, start_r, start_c):
                        # Place the block manually to avoid overhead
                        for dr, dc in orientation:
                            current_grid[start_r + dr][start_c + dc] = b_id
                            
                        if VIDEOFLAG:
                            plot_grid(current_grid, block_colors, b_id)
                            
                        placed_this_block = True
                        break
                
                if placed_this_block:
                    break
            
            if not placed_this_block:
                all_placed = False
                break
        
        if all_placed:
            return current_grid

# Task: Solve an NxN grid puzzle by placing blocks

LEVEL = 0

# ## Define Grid and Blocks
# Initialize an NxN occupancy grid filled with zeros
if LEVEL == 1:
    grid_size = (4,3) #Level 1
if LEVEL == 2:
    grid_size = (6, 4) #Level 2
if LEVEL == 3:
    grid_size = (5, 4) #Level 3
if LEVEL == 4:
    grid_size = (6, 4) #Level 4
if LEVEL == 0:
    grid_size = (8, 7) #Ceasars Palace

grid = np.zeros(grid_size, dtype=int).tolist() # Convert numpy array to list for easier manipulation

if LEVEL == 0:
    #Cells always blacked out
    grid[0][6] = -1
    grid[1][6] = -1
    grid[7][0] = -1
    grid[7][1] = -1
    grid[7][2] = -1
    grid[7][3] = -1
    ##Now the Date
    #grid[1][5] = -1 #December
    grid[0][0] = -1 #January
    #grid[5][6] = -1 #28th
    #grid[2][0] = -1 #1st
    grid[5][1] = -1 #23rd
    #grid[6][3] = -1 #Sun
    #grid[7][4] = -1 #Thursday
    grid[7][5] = -1 #Friday

if LEVEL == 2:
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

block_Lll = [
    (0, 0),
    (1, 0),
    (2, 0), (2, 1),
    (2,2)
]

block_Ll = [
    (0, 0),
    (1, 0),
    (2, 0), 
    (3, 0),
    (3, 1)
]

block_C = [
    (0,0),
    (1,0),
    (2,0),
    (2,1),
    (0,1)
]

block_A = [
    (0,0),
    (1,0),
    (1,1),
    (1,2),
    (2,2)   
]

block_S = [
    (0, 0), (0, 1),
    (1, 0), (1, 1)
]

block_Ss = [
    (0, 0), (0, 1),
    (1, 0), (1, 1),
    (1,2)
]

# Define the shape of the 3x1 block as a list of relative coordinates
block_T = [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 1)
]

block_Tt = [
    (0, 0),
    (0, 1),
    (0, 2),
    (1, 1),
    (2, 1)
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

block_Zz = [
    (0, 0), (0, 1),
            (1, 1), (1, 2),(1,3)
]

# Define block colors
if LEVEL == 0:
    block_colors = {
        1: 'red',
        2: 'blue',
        3: 'yellow',
        4: 'green',
        5: 'orange',
        6: 'cyan',
        7: 'magenta',
        8: 'lime',
        9: 'purple',
        10: 'brown',
    }

if LEVEL == 2:
    block_colors = {
        1: 'red',
        2: 'red',
        3: 'yellow',
        4: 'green',
        5: 'green',
    }   

if LEVEL == 3:
    block_colors = {
        1: 'orange',
        2: 'yellow',
        3: 'cyan',
        4: 'cyan',
        5: 'blue',
    }

if LEVEL == 4:
    block_colors = {
        1: 'red', # block_Z
        2: 'cyan', # block_I (first instance)
        3: 'cyan',  # block_I (second instance)
        4: 'blue',  # block_L
        5: 'purple', # block_T
        6: 'purple' # block_T
    }

if LEVEL == 1:
    block_colors = {
        1: 'blue',
        2: 'purple',
        3: 'purple',
    }

# ## Execute and Display Solution
# Call the solve function with the initial NxN grid, a list of the two blocks, and the starting block ID (e.g., 1). Print the resulting grid if a solution is found, otherwise indicate that no solution exists.
if LEVEL == 0:
    blocks_to_place = [
        (1, block_Zz),
        (2, block_I),
        (3, block_A),
        (4, block_Lll),
        (5, block_Ll),
        (6, block_Ss),
        (7, block_L),
        (8, block_Tt),
        (9, block_C),
        (10, block_Z)
    ]   

if LEVEL == 2:
    blocks_to_place = [
        (1, block_Z),
        (2, block_Z),
        (3, block_S),
        (4, block_Z),
        (5, block_Z),
    ]

if LEVEL == 3:
    blocks_to_place = [
        (1, block_L),
        (2, block_S),
        (3, block_I),
        (4, block_I),
        (5, block_L),
    ]

if LEVEL == 4:
    blocks_to_place = [
        (1, block_Z),
        (2, block_I),
        (3, block_I),
        (4, block_L),
        (5, block_T),
        (6, block_T)
    ]

if LEVEL == 1:
    blocks_to_place = [
        (1, block_L),
        (2, block_T),
        (3, block_T)
    ]

# Visualize blocks and grid before solving
if BLOCKFLAG:
    for block_id, block_shape in blocks_to_place:
        norm_shape = normalize_block_shape(block_shape)
        max_r = max(r for r, c in norm_shape)
        max_c = max(c for r, c in norm_shape)
        temp_grid = np.zeros((max_r + 3, max_c + 3), dtype=int).tolist()
        for r, c in norm_shape:
            temp_grid[r + 1][c + 1] = block_id
        plt.figure(f"Block {block_id}")
        plot_grid(temp_grid, block_colors, current_block_id=block_id, force=True)
    plt.show()

if not MOBILEFLAG:
    plt.figure("Initial Grid")
    plot_grid(grid, block_colors, force=True)
    plt.show()

starting_time = time.time()
solution = solve(grid, blocks_to_place)

end_time = time.time()
print(f"\nTotal solving time: {end_time - starting_time:.4f} seconds\n")

if solution is not None:
    print("Solution Found:")
    for row in solution:
        print(row)
    #plot final solution
    if not MOBILEFLAG:
        plt.figure("Final Solution")
        plot_grid(solution, block_colors, force=True)
        plt.show() # Keep the final plot open
else:
    print("No solution found for the puzzle.")
