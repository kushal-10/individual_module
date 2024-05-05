from MCGrip.environment import GridWorldEnv
from MCGrip.layout import BoardLayout
from utils import generate_utils
from dataset.levels_desc import LEVELS_REGISTRY
from agents.manhattan import manhattan_pathfinder

import numpy as np
import os
from PIL import Image
import json

'''
3) Target loc to center of piece instead of corner
'''
# Level Setup
level = LEVELS_REGISTRY[1] #Use 1 for testing/0 for main
level_name = level["level_name"]
num_distractors = level["num_distractors"]
total_pieces = num_distractors + 1
grid_size = level["grid_size"]
num_boards = level["num_boards"]
multiplier = level["multiplier"]
board_desc = level["boards"]

# Base Information
shapes = np.array(['P', 'T', 'U', 'W', 'X', 'Z'])
seed = 420
np.random.seed(seed)
random_seeds = np.random.randint(0, 200, multiplier)
SAVE_DIR = "data"

# Setup boards
BOARDS = []
for board in board_desc:
    target_color = board_desc[board]["target_color"] 
    for s in random_seeds:
        board_layout = BoardLayout(N=grid_size, num_pieces=total_pieces, shapes=shapes, seed=s)
        agent_pos, grid_info = board_layout.set_board_layout(target_colour=target_color, level=level_name)
        target_pos = grid_info[0]['piece_grids']
        BOARDS.append({"agent_position": agent_pos, "target_position": target_pos, "grid_information": grid_info})

# Check for Data/Levels Folder
level_dir = os.path.join(SAVE_DIR, level_name)
if not os.path.exists(level_dir):
    os.makedirs(level_dir)

for i, board in enumerate(BOARDS):
    board_dir = os.path.join(level_dir, f'board_{i}')
    img_dir = os.path.join(board_dir, 'images')
    txt_dir = os.path.join(board_dir, 'text')

    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(txt_dir, exist_ok=True)

    # Save initial state image
    env = GridWorldEnv(render_mode="rgb_array", size=grid_size, grid_info=board["grid_information"], agent_pos=board["agent_position"], target_pos=board["target_position"])
    observation, info = env.reset()
    initial_image = env.render()
    generate_utils.save_board_images(img_dir, [initial_image], 'step')

    # Save Initial RE
    initial_re = generate_utils.generate_initial_re(board['grid_information'])
    generate_utils.save_as_json({"initial_re": initial_re}, os.path.join(txt_dir, 'initial_re.json'))

    # Get Steps
    steps = manhattan_pathfinder(board['agent_position'], board['target_position'][0])
    steps_dict = generate_utils.generate_steps_dict(steps)

    # Save Steps
    generate_utils.save_as_json(steps_dict, os.path.join(txt_dir, 'steps.json'))

    # Generate and save step images
    for s, action in enumerate(steps):
        observation, _, _, _ = env.step(action)
        step_image = env.render()
        generate_utils.save_board_images(img_dir, [step_image], f'step_{s + 1}')

print("Saved all the generated instances to data")