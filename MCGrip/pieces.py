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

I = [[0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]]

L = [[0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0],
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

V = [[0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0],
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
    'I': I,
    'L': L,
    'N': N,
    'P': P,
    'T': T,
    'U': U,
    'V': V,
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
    def __init__(self, symbol: str, rotation: int, position: np.array, istarget: bool = False):
        self.symbol = symbol
        self.rotation = rotation
        self.position = position
        self.istarget = istarget
        
    def get_grid_locations(self) -> np.array:
        '''
        Get the locations of blocks to mark as a piece in the Pentomino Board Grid
        Returns:
            grid_marks: An np.array containing multiple vectors of length 2
                        co-ordinates to be marked in the Pentomino Board Grid
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
    
    def get_target(self) -> np.array:
        '''
        Get the center of the target piece
        Returns:
            center: A vector of length 2 - co-ordinates of the center of the target piece
        '''
        if not self.istarget:
            raise Exception('This piece is not a target piece')
        center = self.position + np.array([2, 2])
        return center