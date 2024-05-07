from MCGrip.environment import GridWorldEnv
from MCGrip.layout import BoardLayout
from utils import generate_utils
from agents.manhattan import manhattan_pathfinder

import progressbar
import numpy as np
import os

'''
3) Target loc to center of piece instead of corner
4) Sliding WIndow images
'''
# CONSTANTS
SHAPES = ['P', 'T', 'U', 'W', 'X', 'Z']
SAVE_DIR = 'data'

level1_data = generate_utils.load_json(os.path.join('splits', 'easy', 'metadata.json'))
level_name = level1_data['level']
total_pieces = level1_data['num_distractors'] + 1
grid_size = level1_data['grid_size']

def gen_boards(split_name: str):
    BOARDS = []
    split_instances = level1_data[split_name]
    for inst in split_instances:
        piece_regions = [inst['target_position']] + inst['distractor_positions']

        board_layout = BoardLayout(N=grid_size, num_pieces=total_pieces, shapes=SHAPES, seed=inst['seed'])
        agent_pos, grid_info = board_layout.set_board_layout(target_colour = inst['target_colour'],
                                                             target_shape = inst['target_shape'],
                                                             regions = piece_regions,
                                                             level = 'easy')
        target_pos = grid_info[0]['piece_grids']
        BOARDS.append({"agent_position": agent_pos, "target_position": target_pos, "grid_information": grid_info})
    
    return BOARDS


def gen_instances(split_name: str):
    BOARDS = gen_boards(split_name)

    # Check for Data/Levels Folder
    level_dir = os.path.join(SAVE_DIR, level_name, split_name)
    if not os.path.exists(level_dir):
        os.makedirs(level_dir)

    bar = progressbar.ProgressBar(maxval=len(BOARDS)).start()
    for i, board in enumerate(BOARDS):
        board_dir = os.path.join(level_dir, f'board_{i}')
        img_dir = os.path.join(board_dir, 'images')
        txt_dir = os.path.join(board_dir, 'text')

        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(txt_dir, exist_ok=True)

        # Save initial state image
        env = GridWorldEnv(render_mode="rgb_array", size=grid_size, grid_info=board["grid_information"], agent_pos=board["agent_position"], target_pos=board["target_position"])
        _, _ = env.reset()
        initial_image = env.render()
        generate_utils.save_board_images(img_dir, initial_image, 'step_0')

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
            _, _, _, _ = env.step(action)
            step_image = env.render()
            generate_utils.save_board_images(img_dir, step_image, f'step_{s + 1}')
        bar.update(i)

    print(f"Saved all the generated instances for split {split_name} to data/{split_name}")

if __name__ == '__main__':
    # gen_instances('test')
    gen_instances('train')
    gen_instances('validation')