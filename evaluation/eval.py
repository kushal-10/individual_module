"""
TODOS - 1806
1) Use the adapters to do inference on an image
- Try AutoAdapterModel loading for llava1.5 [DONE]

2) Set up evaluation pipeline [ON THIS]
We have a backend up and running, Need to write scoring function/ Metrics
Single flow to generate responses, without multiple times model loading

3) Use the adapters, base model and generate two results
"""

from evaluation.runs import ModelRuns

model_id = "llava-hf/llava-1.5-13b-hf"
adapter_id = "../LLaVA/checkpoints/llava-v1.5-13b-task-lora"

model = ModelRuns(model_id, adapter_id)

prompt = "<image>\nYou are an intelligent agent playing a pentomino game. You are given a board with 20 x 20 grids and a target piece. Your spawn location is represented by the black circle on the board. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the red P shaped piece located on top left of the board. Only respond in one word what next step will you take from ['left', 'right', 'up', 'down', 'grip']\n ASSISTANT:"
image_file = "data/easy/test/board_0/images/step_0.png"
response = model.generate_response(image_file, prompt)
print(f"Response: {response}")

prompt = "<image>\nYou are an intelligent agent playing a pentomino game. You are given a board with 20 x 20 grids and a target piece. Your spawn location is represented by the black circle on the board. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the red P shaped piece located on top left of the board. Only respond in one word what next step will you take from ['left', 'right', 'up', 'down', 'grip']\n ASSISTANT:"
image_file = "data/easy/test/board_0/images/step_1.png"
response = model.generate_response(image_file, prompt)
print(f"Response: {response}")

prompt = "<image>\nYou are an intelligent agent playing a pentomino game. You are given a board with 20 x 20 grids and a target piece. Your spawn location is represented by the black circle on the board. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the red P shaped piece located on top left of the board. Only respond in one word what next step will you take from ['left', 'right', 'up', 'down', 'grip']\n ASSISTANT:"
image_file = "data/easy/test/board_0/images/step_2.png"
response = model.generate_response(image_file, prompt)
print(f"Response: {response}")



