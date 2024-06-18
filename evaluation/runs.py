# Model Runs, Save output

"""
Output Format
model_id | generated_value | gold_truth | board_number | image |
"""
import os
import progressbar

from evaluation.backend import ModelRuns

# prompt = "<image>\nYou are an intelligent agent playing a pentomino game. You are given a board with 20 x 20 grids and a target piece. Your spawn location is represented by the black circle on the board. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the red P shaped piece located on top left of the board. Only respond in one word what next step will you take from ['left', 'right', 'up', 'grip', 'down']\n ASSISTANT:"
# image_file = "data/easy/test/board_0/images/step_0.png"
# response = model.generate_response(image_file, prompt)
# print(f"Response: {response}")


if __name__ == "__main__":
    model_id = "llava-hf/llava-1.5-13b-hf"
    adapter_id = "../LLaVA/checkpoints/llava-v1.5-13b-task-lora"

    # Initialize Model
    # base_model = ModelRuns(model_id)
    adapter_model = ModelRuns(model_id, adapter_id)

    # Initialize locations
    root = 'data'
    level = 'easy'
    split = 'test'
    split_dir = os.path.join(root, level, split)
    boards = os.listdir(split_dir)

    # Initialize data to collect
    save_name = 'llava15_adapter_test.csv'
    actions = []
    gts = []
    board_numbers = []
    image_numbers = []

    bar = progressbar.ProgressBar(maxval=len(boards)).start()
    for i, board in enumerate(boards):
        image_dir = os.path.join(split_dir, board, images)
        image_paths = os.listdir(image_dir)

        # Get prompt (Should be same for all images)
        # Get prompt + Ground truth values
        text_dir = os.path.join(split_dir, board, text)

        for image_path in image_paths:
            # At single instance level
            # Get full path of the image
            input_path = os.path.join(image_dir, image_path)
            img_no = image_path.split('.')[0].split('_')[-1]
            image_numbers.append(img_no) # Get Image number value







        board_number = board.split('_')[-1]
        bar.update(i)





