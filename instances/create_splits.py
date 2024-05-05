# Create splits for 'easy' level
from utils import generate_utils

import os
import numpy as np

np.random.seed(42)

COLOURS = ['red', 'blue', 'green', 'purple', 'brown', 'yellow']
SHAPES = ['P', 'T', 'U', 'W', 'X', 'Z']
POSITIONS = ['top left', 'top', 'top right', 'left', 'right', 'bottom left', 'bottom', 'bottom right']
MULTIPLIER = 10 # How many boards of silmilar target piece (same colour/shape/positions) should be there

SPLITS = {
    'level': 'easy',
    'num_distractors': 3,
    'grid_size': 20,
    'train': [],
    'test': [],
    'validation': []
}

for colour in COLOURS:
    for shape in SHAPES:
        for pos in POSITIONS:
            for i in range(MULTIPLIER):
                # Remove the position of target piece 
                temp_positions = ['top left', 'top', 'top right', 'left', 'right', 'bottom left', 'bottom', 'bottom right'] 
                temp_positions.remove(pos) 

                # Select unique positions of distractors randomly
                random_positions = np.random.choice(temp_positions, size=SPLITS['num_distractors'], replace=False)
                random_positions = random_positions.tolist()
                
                # Select a random seed value
                random_seed = np.random.randint(0, 1000)
                data = {
                    'target_position': pos,
                    'target_colour': colour,
                    'target_shape': shape,
                    'distractor_positions': random_positions, 
                    'seed': random_seed
                }

                # Even distribution in all three splits - 6, 2, 2 per target piece
                if i <= 5:
                    SPLITS['train'].append(data)
                elif i > 5 and i <= 7:
                    SPLITS['test'].append(data)
                else:
                    SPLITS['validation'].append(data)

save_path =  os.path.join('splits', SPLITS['level'], 'metadata.json')
generate_utils.save_as_json(SPLITS, save_path)
print(f"Splits Generated - Saved to {save_path}")