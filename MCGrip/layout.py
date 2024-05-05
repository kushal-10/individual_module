import numpy as np

from MCGrip.pieces import PentominoPiece
from MCGrip.definitions import COLOURS, COLOUR_NAMES
from utils import layout_utils
import math

# Setting the layout fixed for now i.e start positions of each piece are at every 5x5 grid
class BoardLayout():
    '''
    This class is used to generate a random layout of pentomino pieces on a board.
    Args:
        N: The size of the Pentomino Board Grid
        num_pieces: The number of pieces to be placed on the board
        shapes: A list of the pentomino shapes to be selected from
    '''
    def __init__(self, N: int, num_pieces: int, shapes: np.array, seed: int) -> None:
        self.N = N
        self.num_pieces = num_pieces
        self.shapes = shapes
        self.mapped_regions = layout_utils.map_regions(self.N, pad=0)
        np.random.seed(seed)
    
    def set_start_positions(self, regions: str = None) -> np.array:
        '''
        Get start positions of everything on the board
        Args:
            regions: A list defining the regions where the piece will be spawned (['top', 'top left', 'right',...])
        Returns:
            all_start_positions - [[ax, ay], [p1x, p1y], [p2x, p2y], ....]
            The starting positions of agents and all the pieces (top left corner of 5x5 grid)
        '''

        center_sq = math.ceil((self.N)/2)
        agent_start_pos = np.array([center_sq - 1, center_sq - 1], dtype=np.int64) # Sub 1 to make this top-left corner of center grid
        # Set the starting position at the center of the grid where the gripper will be spawned

        # Use this location to check for overlaps for new pieces generated
        all_start_positions = np.array([agent_start_pos])

        for i in range(self.num_pieces):
            # Select a random start position for each piece
            if regions:
                # Add a check to ensure num_pieces = len(region)
                assert self.num_pieces == len(regions), "Defined number of regions should be equal to defined number of pieces"
                region_choices = self.mapped_regions[regions[i]] # Get possible spawn locations for a specific region
            else:
                region_choices = [[x, y] for x in range(self.N) for y in range(self.N)] # Get possible spawn locations across the board

            random_choice = np.random.randint(0, len(region_choices)) # Select a random index
            piece_start_pos = region_choices[random_choice] # Random grid mark in the specified region

            # Draw randomly, until a valid value is found
            # This ensures no overlaps between pieces and center grid (central 3x3 will always be empty) 
            while not layout_utils.valid(self.N, piece_start_pos, all_start_positions, spacing=0):
                # Remove invalid starting position and select a start position again
                region_choices.remove(piece_start_pos) 
                random_choice = np.random.randint(0, len(region_choices)) 
                piece_start_pos = region_choices[random_choice] 
            all_start_positions = np.vstack((all_start_positions, piece_start_pos))

        return all_start_positions

    def set_board_layout(self, target_symbol=None, target_colour=None, regions=None, level=None):
        all_start_positions = self.set_start_positions(regions)
        agent_start_pos = all_start_positions[0] + 1 # Make the start location of the agent back to center of the grid from top left corner 
        grid_info = []
        available_shapes = list(self.shapes)  # List of available shapes
        available_colours = list(COLOUR_NAMES)  # List of available colours

        for i in range(1, len(all_start_positions)):
            piece_position = all_start_positions[i]

            # Select a random symbol from the available shapes
            piece_symbol = np.random.choice(available_shapes)
            if i == 1 and target_symbol:
                piece_symbol = target_symbol  # Overwrite target symbol if specified
            if level == "easy":
                available_shapes.remove(piece_symbol)  # Remove the selected symbol from the available shapes, Only for easy level

            # Select a random colour from the available colours
            piece_colour = np.random.choice(available_colours)
            if i == 1 and target_colour:
                piece_colour = target_colour  # Overwrite target colour if specified
            if level == "easy":
                available_colours.remove(piece_colour)  # Remove the selected colour from the available colours, Only for easy level

            piece_rotation = 0  # No rotation for now

            piece = PentominoPiece(piece_symbol, piece_rotation, piece_position)
            piece_grids = piece.get_grid_locations()
            piece_region = regions[i-1]
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


if __name__ == '__main__':
    boardtemp = BoardLayout(10, 4, ['P', 'T', 'U', 'W', 'X', 'Z'], 69420)
    info = boardtemp.set_board_layout(
        target_symbol = 'P',
        target_colour = 'red',
        regions = ['top', 'bottom', 'left', 'right'],
        level = 'easy')
    
    print(info)

                  

