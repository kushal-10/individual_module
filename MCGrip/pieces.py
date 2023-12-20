# Define the pentomino pieces and handle their rotations
# Output should be an array/list of 1x2 blocks to be marked in the pentomino grid environment

import numpy as np

# Piece definitions for 0 rotation
# Pieces are F, I, L, N, P, T, U, V, W, X, Y, Z

F = [[0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]]

N = [[0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]]

P = [[0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0]]

T = [[0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0]]

U = [[0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0]]

W = [[0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]]

X = [[0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]]

Y = [[0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0]]

Z = [[0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]]

# Create a dictionary item for the pieces
pieces_dict = {
    'F': F,
    'N': N,
    'P': P,
    'T': T,
    'U': U,
    'W': W,
    'X': X,
    'Y': Y,
    'Z': Z
}

class PentominoPiece():
    '''
    Intialize a pentomino piece with a symbol, rotation and position
    Args:
        symbol: A single letter string correesponding to the piece shape
        rotation: An integer r in {0, 1, 2, 3} to define the angle of rotation corresponding to  r*pi/2
        position: The block in the Pentomino Board Grid coressponding to the top left corner of the Piece Grid
    '''
    def __init__(self, symbol: str, rotation: int, position: np.array):
        self.symbol = symbol
        self.rotation = rotation
        self.position = position
        
    def get_grid_locations(self) -> np.array:
        '''
        Get the locations of blocks to mark as a piece in the Pentomino Board Grid
        Returns:
            grid_marks: An np.array containing multiple vectors of length 2 for a single piece
                        (co-ordinates to be marked in the Pentomino Board Grid)
        '''
        
        default_piece_grid = pieces_dict[self.symbol]
        rotated_piece_grid = np.rot90(default_piece_grid, self.rotation)

        grid_marks = []
        for i in range(rotated_piece_grid.shape[0]):
            for j in range(rotated_piece_grid.shape[1]):
                if rotated_piece_grid[i][j] == 1:
                    grid_marks.append(self.position + np.array([i, j]))
        grid_marks = np.array(grid_marks)

        return grid_marks
    
    def get_region(self, agent_start_pos, piece_start_pos):
        '''
        Get the region of the piece w.r.t. the center of Pentomino board
        Possible regions - top left, top, top right, left, right, bottom left, bottom, bottom right
        Args:
            agent_start_pos = The center of the Agent block (Should be 5x5 grid at the center of the board)
            piece_start_pos = Co-ordinates of the top-left square of the 5x5 Piece block
        Returns:
            result = A string like "top left" or "bottom" out of 8 possible regions 
        '''
        pos_x = piece_start_pos[0]
        pos_y = piece_start_pos[1]
        ax1 = agent_start_pos[0] - 2
        ay1 = agent_start_pos[1] - 2
        ax2 = ax1 + 4
        ay2 = ay1 + 4

        result = ""
        if pos_x <= ax1:
            result += "left"
            
        if pos_x >= ax2:
            result += "right"

        if pos_y <= ay1:
            if result == "":
                result += "top"
            else:
                result = "top" + " " + result

        if pos_y >= ay2:
            if result == "":
                result += "bottom"
            else:
                result = "bottom" + " " + result

        return result
    