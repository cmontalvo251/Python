import random
import matplotlib.pyplot as plt
import textwrap

# This is also in Google Colab on Google Drive in the Scripts folder

# --- 1. BINGO ITEM DATABASE (Data moved from bingo_data.py) ---

"""
This dictionary contains the 75 custom Bingo items organized by column.
B: 1-15, I: 16-30, N: 31-45, G: 46-60, O: 61-75
"""
BINGO_ITEMS = {
    # --- B Column (Items 1-15) ---
    'B': [
        "L gets her licenses",
        "Someone gets married",
        "Someone goes to jail",
        "Record heat",
        "Vehicle breaks down",
        "Someone gets an award",
        "Record drought",
        "Record rainfall",
        "Record freeze",
        "Hurricane hits close by",
        "Parents get CO",
        "C gets promoted",
        "Someone loses a tooth",
        "E starts her period",
        "Someone breaks a bone",
    ],

    # --- I Column (Items 16-30) ---
    'I': [
        "Someone goes to the hospital",
        "Someone has surgery",
        "Someone gets braces",
        "Gov't shutdown",
        "Someone buys a new vehicle",
        "School closes due to major weather",
        "Trump does something stupid",
        "Someone gets a new job",
        "Someone gets a piercing",
        "Someone travels internationally",
        "Someone finishes a long race",
        "Someone graduates",
        "L reads a chapter book alone",
        "Li moves out",
        "Someone gets a new hobby",
    ],

    # --- N Column (Items 31-45) ---
    'N': [
        "Someone sells a house",
        "Someone gets a certification",
        "Someone gets on TV",
        "Someone gets shipped",
        "Someone calls 911",
        "Someone gets a tattoo",
        "C hikes a Highest Peak (HP)",
        "N gets a kidney",
        "A finishes her large book",
        "Someone learns Spanish",
        "Charlie King's wife marries JD vance",
        "Someone dyes their hair",
        "Li gets a bathroom",
        "Someone renovates their house",
        "Someone moves",
    ],

    # --- G Column (Items 46-60) ---
    'G': [
        "Someone invents something",
        "Someone gets a new pet",
        "Someone wins money",
        "Animals make the news",
        "A conspiracy theory ends up true",
        "Someone starts a business",
        "Someone shaves their head",
        "Someone plays a concert",
        "Someone retires",
        "Artemis II successfully launches",
        "Starship lands successfully",
        "Alabama makes national news",
        "A child under 12 uses a curse word",
        "Ms harvest a pineapple",
        "Gov't official dies of natural causes",
    ],

    # --- O Column (Items 61-75) ---
    'O': [
        "Someone gets fired",
        "Someone gets engaged",
        "Someone gets into a fist fight",
        "Someone's phone stops working",
        "Someone has a baby",
        "Political Assassination",
        "Epstein files will be released",
        "A large meteor will crash into Earth",
        "Hollywood moves to TX",
        "Someone goes to physical therapy",
        "School closes due to a weather event",
        "Family plays pickleball @ parents house",
        "Someone gets on a podcast",
        "Americans enter war",
        "Someone gets a new hobby",
    ],
}

# --- 2. BINGO CARD GENERATION FUNCTIONS ---

def generate_bingo_card(items_data: dict) -> dict:
    """
    Generates a single, randomized 5x5 Bingo card using the provided item data.
    """
    card = {}
    columns = ['B', 'I', 'N', 'G', 'O']

    for col in columns:
        item_pool = items_data[col]

        if col == 'N':
            # 'N' column requires only 4 randomized items + 1 FREE SPACE
            selected_items = random.sample(item_pool, 4)
            # Insert the FREE SPACE into the center (index 2)
            selected_items.insert(2, "FREE SPACE")
            card[col] = selected_items
        else:
            # All other columns ('B', 'I', 'G', 'O') require 5 randomized items
            card[col] = random.sample(item_pool, 5)

    return card

def display_card(card: dict):
    """
    Generates and displays the Bingo card as a matplotlib figure.
    """

    # Character limit for text wrapping inside the cell
    MAX_LINE_WIDTH = 15

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_title("Custom 5x5 Bingo Card", fontsize=18, pad=20)
    ax.axis('off') # Hide the axes

    columns = ['B', 'I', 'N', 'G', 'O']
    num_cols = len(columns)
    num_rows = 5 # Always 5 rows for Bingo

    # Set up the grid space from (0,0) to (num_cols, num_rows)
    ax.set_xlim(0, num_cols)
    ax.set_ylim(0, num_rows + 1) # Extra space for the title/headers

    # Draw the grid lines and header labels
    for i in range(num_cols + 1):
        # Vertical lines
        ax.plot([i, i], [0, num_rows], color='black', linewidth=2)
        # Horizontal lines (including top and bottom)
        ax.plot([0, num_cols], [i, i], color='black', linewidth=2)

    # Place the BINGO header letters
    for i, col_letter in enumerate(columns):
        # Header text is centered above the column
        ax.text(i + 0.5, num_rows + 0.5, col_letter, ha='center', va='center',
                fontsize=24, fontweight='bold', color='darkred')

    # Iterate through the card data and place the text
    for i, col_letter in enumerate(columns):
        for j in range(num_rows):
            item = card[col_letter][j]
            x_coord = i + 0.5
            # Y coordinates are inverted to display from top-to-bottom
            y_coord = num_rows - j - 0.5

            # Customize the FREE SPACE text
            if item == "FREE SPACE":
                text_color = 'green'
                font_weight = 'extra bold'
                font_size = 14
                
                # Draw a star or highlight the free space cell
                ax.fill([i, i+1, i+1, i], [num_rows - j - 1, num_rows - j - 1, num_rows - j, num_rows - j], 
                        color='lightyellow', alpha=0.6)
                
                wrapped_item = item
            else:
                text_color = 'black'
                font_weight = 'normal'
                font_size = 10

                # --- Text Wrapping Logic ---
                # Use textwrap.fill to insert newlines into the string
                wrapped_item = textwrap.fill(item, width=MAX_LINE_WIDTH)

            # Use ax.text to place the wrapped item string
            ax.text(x_coord, y_coord, wrapped_item, ha='center', va='center',
                    fontsize=font_size, fontweight=font_weight, color=text_color,
                    linespacing=1.2)

    plt.show()

# --- 3. EXECUTION ---

if __name__ == "__main__":
    # 1. Generate the card
    my_card = generate_bingo_card(BINGO_ITEMS)

    # 2. Display the card using matplotlib
    display_card(my_card)