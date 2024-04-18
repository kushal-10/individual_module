from MCGrip.environment import GridWorldEnv
from MCGrip.layout import BoardLayout
from dataset.levels_desc import LEVELS_REGISTRY
from agents.manhattan import shortest_path

import numpy as np
import os

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
seed = 42
np.random.seed(seed)
random_seeds = np.random.randint(0, 200, multiplier)

# Setup boards
BOARDS = []
for board in board_desc:
    target_color = board_desc[board]["target_color"]
    for s in random_seeds:
        board = BoardLayout(N=grid_size, num_pieces=total_pieces, symbols=shapes, seed=s)
        AGENT_POS, grid_info = board.set_board_layout(target_colour=target_color, level="easy")
        TARGET_POS = grid_info[0]['piece_grids']
        BOARDS.append({"agent_position": AGENT_POS, "target_position": TARGET_POS, "grid_information": grid_info})

for i, board in enumerate(BOARDS):
    if i==0:
        env = GridWorldEnv(render_mode="human", size=grid_size, grid_info=board["grid_information"], agent_pos=board["agent_position"], target_pos=board["target_position"])
        observation, info = env.reset()

        POS = board['grid_information'][0]['piece_region']
        COL = board['grid_information'][0]['piece_colour']
        SHP = board['grid_information'][0]['piece_symbol']
        initial_re = f"take the {COL} {SHP} on {POS}"
        print(initial_re)

        steps = shortest_path(board['agent_position'], board['target_position'][0])

        for i in range(len(steps)):
            action = steps[i]
            observation, reward, done, info = env.step(action)
