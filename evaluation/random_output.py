import pandas as pd
import random

df = pd.read_csv('results/base_prompt1.csv')
n = len(df)
actions = ['left', 'right', 'up', 'down', 'grip']

random_predictions = []

for i in range(n):
    random_action = random.choice(actions)
    random_predictions.append(random_action)

df['actions'] = random_predictions

df.to_csv('results/random_output.csv', index=False)