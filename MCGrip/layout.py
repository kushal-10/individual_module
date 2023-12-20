
import numpy as np
from MCGrip.pieces import PentominoPiece
from MCGrip.definitions import COLOURS, COLOUR_NAMES

seed = 42
np.random.seed(seed)

# Setting the layout fixed for now i.e start positions of each piece are at every 5x5 grid

class BoardLayout():
    '''
    This class is used to generate a random layout of pentomino pieces on a board.
    Args:
        N: The size of the Pentomino Board Grid
        num_pieces: The number of pieces to be placed on the board
        symbols: A list of the pentomino symbols to be selected from
    '''
    def __init__(self, N: int, num_pieces: int, symbols: np.array) -> None:
        self.N = N
        self.num_pieces = num_pieces
        self.symbols = symbols

    def valid(self, p1, pos):
        '''
        Checks if a top-left corner of a new piece is valid on the board or not
        Args:
            p1 - The top-left corner co-ordinate of a piece block
            pos - A list of top-left corners of previous generated blocks
                - to check for overlap
        '''
        result = 0
        for p2 in pos:
            # For each previously assigned piece get the difference between top-left corners of each
            diff_x = abs(p1[0] - p2[0])
            diff_y = abs(p1[1] - p2[1]) 
            if diff_x + diff_y > 4: # No overlap of 5x5 Piece grids
                if p1[0] <= self.N - 5 and p1[1] <= self.N - 5 and p2[0] <= self.N - 5 and p2[1] <= self.N - 5: # Piece inside boundaries
                    result += 0
                else:
                    result += 1   
            else:
                result += 1

        if not result:
            return True
        else:
            return False
        
    def set_start_positions(self) -> np.array:
        '''
        Get start positions of everything on the board
        Returns:
            all_start_positions - [[ax, ay], [p1x, p1y], [p2x, p2y], ....]
            The starting positions of agents and all the pieces (top left corner of 5x5 grid)
        '''

        center_sq = (self.N)/2
        agent_start_pos = np.array([center_sq-2, center_sq-2], dtype=np.int64)
        # Set the starting position at the top-left corner of the central 5x5 grid where the gripper will be spawned
        # Use this location to check for overlaps for new pieces generated
        all_start_positions = np.array([agent_start_pos])

        for i in range(self.num_pieces):
            # Select a random start position for each piece
            piece_start_pos = np.random.randint(0, self.N, size=2)

            # Draw randomly, until a valid value is found
            while not self.valid(piece_start_pos, all_start_positions):
                piece_start_pos = np.random.randint(0, self.N, size=2)
            all_start_positions = np.vstack((all_start_positions, piece_start_pos))

        return all_start_positions

    def set_board_layout(self):
        all_start_positions = self.set_start_positions()
        agent_start_pos = all_start_positions[0] + 2 # Add 2, to get the center of agent block
        grid_info = []
        for i in range(1, len(all_start_positions)):
            piece_position = all_start_positions[i]
            piece_symbol = np.random.choice(list(self.symbols))
            # piece_rotation = np.random.randint(0, 4)
            piece_rotation = 0 # No rotation for now
            piece_colour = np.random.choice(COLOUR_NAMES)

            piece = PentominoPiece(piece_symbol, piece_rotation, piece_position)
            piece_grids = piece.get_grid_locations()
            piece_region = piece.get_region(agent_start_pos, piece_position)
            piece_data = {
                "piece_grids": piece_grids,
                "piece_colour": piece_colour,
                "colour_value": COLOURS[piece_colour],
                "start_position": piece_position,
                "piece_symbol": piece_symbol,
                "piece_rotation": piece_rotation,
                "piece_region": piece_region 
            }

            grid_info.append(piece_data)

        return agent_start_pos, grid_info

                  

