from MCGrip.environment import GridWorldEnv
from MCGrip.layout import BoardLayout
from dataset.levels_desc import LEVELS_REGISTRY
from agents.manhattan import shortest_path

import numpy as np
import os
from PIL import Image
import json

'''
1) Setup helper function to save as json
2) helper function for transpose and save image
3)
'''

# Level Setup
level = LEVELS_REGISTRY[0]
level_name = level["level_name"]
num_distractors = level["num_distractors"]
total_pieces = num_distractors + 1
grid_size = level["grid_size"]
num_boards = level["num_boards"]
multiplier = level["multiplier"]
board_desc = level["boards"]

#Base Information
shapes = np.array(['P', 'T', 'U', 'W', 'X', 'Z'])
seed = 420
np.random.seed(seed)
random_seeds = np.random.randint(0, 200, multiplier)

# Setup boards
BOARDS = []
for board in board_desc:
    target_color = board_desc[board]["target_color"] 
    for s in random_seeds:
        board = BoardLayout(N=grid_size, num_pieces=total_pieces, shapes=shapes, seed=s)
        AGENT_POS, grid_info = board.set_board_layout(target_colour=target_color, level=level_name)
        TARGET_POS = grid_info[0]['piece_grids']
        BOARDS.append({"agent_position": AGENT_POS, "target_position": TARGET_POS, "grid_information": grid_info})

# Check for Data/Levels Folder
if not os.path.exists(os.path.join('data', level_name)):
    os.makedirs(os.path.join('data', level_name))

for i, board in enumerate(BOARDS):
    env = GridWorldEnv(render_mode="rgb_array", size=grid_size, grid_info=board["grid_information"], agent_pos=board["agent_position"], target_pos=board["target_position"])
    observation, info = env.reset()

    if not os.path.exists(os.path.join('data', level_name, f'board_{i}')):
        os.mkdir(os.path.join('data', level_name, f'board_{i}'))
        os.mkdir(os.path.join('data', level_name, f'board_{i}', 'images')) #create image directory
        os.mkdir(os.path.join('data', level_name, f'board_{i}', 'text')) #create text directory to save Initial RE + Steps

    img_dir = os.path.join('data', level_name, f'board_{i}', 'images')
    txt_dir = os.path.join('data', level_name, f'board_{i}', 'text')

    initial_image = env.render()
    if initial_image is not None:
        initial_image = Image.fromarray(initial_image)
        initial_image = initial_image.transpose(Image.FLIP_LEFT_RIGHT)  # Mirror horizontally
        initial_image = initial_image.transpose(Image.ROTATE_90)  # Rotate 90 degrees clockwise
        initial_image.save(os.path.join(img_dir, f'step_{i + 1}.png'))
    else:
        print("Failed to render initial state")

    POS = board['grid_information'][0]['piece_region']
    COL = board['grid_information'][0]['piece_colour']
    SHP = board['grid_information'][0]['piece_symbol']
    initial_re = f"take the {COL} {SHP} on {POS}"
    re_dict = {
        "initial_re": initial_re
    }

    # Save Initial RE:
    re_path = os.path.join(txt_dir, 'initial_re.json')
    with open(re_path, 'w') as json_file:
        json.dump(re_dict, json_file)

    # New mapping based on the transposed image
    # Right - 1, Left- 3, Up - 2, Down - 0
    ACTION_TO_DIR = {0: "down", 1: "right", 2: "up", 3: "left"}

    # Get Steps    
    steps = shortest_path(board['agent_position'], board['target_position'][0])

    steps_dict = {}
    for n, step_value in enumerate(steps):
        steps_dict[f"step_{n}"] = ACTION_TO_DIR[step_value]

    # Save steps:
    steps_path = os.path.join(txt_dir, 'steps.json')
    with open(steps_path, 'w') as json_file:
        json.dump(steps_dict, json_file)

    for s in range(len(steps)):
        action = steps[s]
        observation, reward, done, info = env.step(action)
        step_image = env.render()

        if step_image is not None:
            generated_image = Image.fromarray(step_image)
            generated_image = generated_image.transpose(Image.FLIP_LEFT_RIGHT)  # Mirror horizontally
            generated_image = generated_image.transpose(Image.ROTATE_90)  # Rotate 90 degrees clockwise
            generated_image.save(os.path.join(img_dir, f'step_{s + 1}.png'))
        else:
            print(f"Failed to render step {s + 1}")


print("Saved all the generated instances to data")


