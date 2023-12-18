from MCGrip.environment import GridWorldEnv

env = GridWorldEnv(render_mode="human", size=20)
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    print(observation, reward, done, info)
    # if done:
    #     break

env.close()
