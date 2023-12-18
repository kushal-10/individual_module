
import numpy as np
from MCGrip.pieces import PentominoPiece
from MCGrip.definitions import COLOURS, START_POS_20

seed = 42
np.random.seed(seed)

# Setting the layout fixed for now i.e start positions of each piece are at every 5x5 grid

class BoardLayout():
    '''
    This class is used to generate a random layout of pentomino pieces on a board.
    Args:
        num_pieces: The number of pieces to be placed on the board
        symbols: A list of the pentomino symbols to be selected from
    '''
    def __init__(self, num_pieces: int, symbols: np.array) -> None:
        self.num_pieces = num_pieces
        self.symbols = symbols
        

    def get_piece_info(self, piece_start_positions: np.array) -> np.array:        
        position_index = np.random.randint(0, 16) # Hardcoded for now (16) for 20x20 board
        if position_index in piece_start_positions:
            while position_index in piece_start_positions:
                position_index = np.random.randint(0, 16)
        piece_start_positions = np.append(piece_start_positions, position_index)

        position = START_POS_20[position_index]
        symbol = np.random.choice(self.symbols)
        rotation = np.random.randint(4)
        colour = COLOURS[np.random.choice(list(COLOURS.keys()))]

        return symbol, rotation, position, colour, piece_start_positions

    def set_layout(self):
        '''
        This method sets a random layout of pentomino pieces on a board.
        '''
        grid_info = []

        # Define start positions of each piece to check for overlaps
        peice_start_positions = np.array([])

        # Set a target piece
        target_symbol, target_rotation, target_position, target_color, peice_start_positions = self.get_piece_info(peice_start_positions)
        target_piece = PentominoPiece(target_symbol, target_rotation, target_position, istarget=True)
        target_grids = target_piece.get_grid_locations()
        target_center = target_piece.get_target()

        target_dict = {
            "target_grid": target_grids,
            "target_color": target_color,
            "target_center": target_center
        }

        grid_info.append(target_dict)

        for _ in range(self.num_pieces - 1):
            symbol, rotation, position, colour, peice_start_positions = self.get_piece_info(peice_start_positions)
            piece = PentominoPiece(symbol, rotation, position)
            piece_grids = piece.get_grid_locations()
            # grid_info = np.append(grid_info, [piece_grids, colour])

            piece_dict = {
                "piece_grid": piece_grids,
                "piece_color": colour
            }

            grid_info.append(piece_dict)

        return grid_info
    