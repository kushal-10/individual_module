from MCGrip.environment import GridWorldEnv
from MCGrip.layout import BoardLayout
import numpy as np

# Environment Controls
num_distractors = 3
total_pieces = num_distractors + 1
grid_size = 20
shapes = np.array(['P', 'T', 'U', 'W', 'X', 'Z'])

board1 = BoardLayout(N=grid_size, num_pieces=total_pieces, symbols=shapes, seed=4)

AGENT_POS, grid_info = board1.set_board_layout(target_colour='red')

TARGET_POS = grid_info[0]['piece_grids']


env = GridWorldEnv(render_mode="human", size=20, grid_info=grid_info, agent_pos=AGENT_POS, target_pos=TARGET_POS)
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    print(observation, reward, done, info)
    # if done:
    #     break

env.close()
