# Helper functions for layout.py
import math

def valid(N: int, p1: list, pos: list, spacing: int = 0) -> bool:
    '''
    Checks if a top-left corner of a new piece is valid on the board or not
    Args:
        N - Size of the board
        p1 - The top-left corner co-ordinate of a piece block
        pos - A list of top-left corners of previous generated blocks
            - to check for overlap
        spacing - An integral value to decide the minimum number of spaces in between two blocks
                - if set to 0, pieces may spawn next to each other
    '''
    check = 0
    piece_size = 3 # Each piece is a 3x3 grid
    for p2 in pos:
        # For each previously assigned piece get the difference between top-left corners of each
        diff_x = abs(p1[0] - p2[0])
        diff_y = abs(p1[1] - p2[1]) 
        if diff_x + diff_y > piece_size - 1 + spacing: # No overlap of 3x3 Piece grids + defined spacing
            if p1[0] <= N - piece_size and p1[1] <= N - piece_size: # Piece inside boundaries
                check += 0
            else:
                check += 1   
        else:
            check += 1

    if not check:
        return True
    else:
        return False
    
    
def map_regions(N: int, pad : int = 0) -> dict:
    '''
    Based on the Grid Size of the board, map grid location to its region (top, bottom, top-left ...)
    Args:
        N - Size of the board
        pad - Size of pad around the center 3x3 grid for setting regions. 
            Example if pad = 0 for a 9x9 grid size, 'left' will be considered from x=[0, 2]
                    if pad = 1 for a 9x9 grid size, 'left' will be considered from x=[0, 1]

    Returns:
        region_map - A dictionary mapping each grid point to it region
    '''

    region_map = {
        'top left': [], 'top': [], 'top right': [], 'left': [], 'right': [], 'bottom left': [], 'bottom': [], 'bottom right': []
    }

    C = math.floor(N/2) # Center grid value
    bound1 = C - 1 - pad
    bound2 = C + 1 + pad

    for x in range(N):
        for y in range(N):
            if x < bound1 and y < bound1:
                region_map['top left'].append([x, y])
            elif x < bound1 and y >= bound1 and y <= bound2:
                region_map['left'].append([x, y])
            elif x < bound1 and y > bound2:
                region_map['bottom left'].append([x, y])
            elif x >= bound1 and x <= bound2 and y < bound1:
                region_map['top'].append([x, y])
            elif x >= bound1 and x <= bound2 and y > bound2:
                region_map['bottom'].append([x, y])
            elif x > bound2 and y < bound1:
                region_map['top right'].append([x, y])
            elif x > bound2 and y > bound2:
                region_map['bottom right'].append([x, y])
            elif x > bound2 and y >= bound1 and y <= bound2:
                region_map['right'].append([x, y])
            
    return region_map
