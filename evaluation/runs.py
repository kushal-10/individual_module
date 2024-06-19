# Model Runs, Save output

import os
import progressbar
import pandas as pd
from tqdm import tqdm

from evaluation.backend import ModelRuns
from utils import generate_utils

if __name__ == "__main__":
    model_id = "llava-hf/llava-1.5-13b-hf"
    adapter_id = "../LLaVA/checkpoints/llava-v1.5-13b-task-lora"

    # Initialize Model
    base_model = ModelRuns(model_id)
    # adapter_model = ModelRuns(model_id, adapter_id)

    eval_model = base_model

    # Initialize locations
    root = 'data'
    level = 'easy'
    split = 'test'
    split_dir = os.path.join(root, level, split)
    boards = os.listdir(split_dir)
    boards.sort()

    # Initialize data to collect
    save_name = 'base_prompt1.csv'
    actions = []
    gts = []
    board_numbers = []
    image_numbers = []

    bar = progressbar.ProgressBar(maxval=len(boards)).start()
    for board in tqdm(boards, desc="Processing Boards"):
        image_dir = os.path.join(split_dir, board, "images")
        image_paths = os.listdir(image_dir)
        image_paths.sort()

        # Get prompt (Should be same for all images)
        # Get prompt + Ground truth values
        text_dir = os.path.join(split_dir, board, "text")

        # Load steps and Initial RE
        steps = generate_utils.load_json(os.path.join(text_dir, 'steps.json'))
        initial_re_json = generate_utils.load_json(os.path.join(text_dir, 'initial_re.json'))
        initial_re = initial_re_json['initial_re']

        # Generate prompt from initial RE
        re_split = initial_re.split()
        colour = re_split[2]
        shape = re_split[3]
        position = re_split[5]
        if len(re_split) == 7:
            position += ' ' + re_split[6]
        # prompt = f"<image>\nYou are an intelligent agent playing a pentomino game. You are given a board with 20 x 20 grids and a target piece. Your spawn location is represented by the black circle on the board. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the {colour} {shape} shaped piece located on {position} of the board. Only respond in one word what next step will you take from ['left', 'right', 'up', 'down', 'grip']\nASSISTANT:"

        # Optimized
        prompt = f"USER: <image>\nYou are given a board with 20 x 20 grids and a target piece. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your spawn location is represented by the black circle on the board and you can only move ['left', 'right', 'up', 'down'] - Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the {colour} {shape} shaped piece located on {position} of the board. Only respond in one word.\nASSISTANT:"

        #GPT
        # prompt = f"USER: <image>\nNavigate a 20x20 grid board to grip the {colour} {shape} piece at {position}. Avoid distractor pieces resembling ['P', 'T', 'U', 'W', 'X', 'Z']. Start at the black circle; move ['grip', 'left', 'right', 'up', 'down']. Respond with your next move in only one word.\nASSISTANT:"


        for image_path in image_paths:
            # At single instance level
            # Get full path of the image
            input_path = os.path.join(image_dir, image_path)
            img_no = image_path.split('.')[0].split('_')[-1]
            image_numbers.append(img_no) # Get Image number value
            step_value = image_path.split('.')[0]
            ground_truth = steps[step_value]
            gts.append(ground_truth)

            # Generate response:
            prediction = eval_model.generate_response(input_path, prompt)
            print(prediction)
            actions.append(prediction)

            board_no = board.split('_')[-1]
            board_numbers.append(board_no) # Get Board number vale, for episodic evaluation

    eval_data = {
        'actions': actions,
        'ground_truths': gts,
        'board_numbers': board_numbers,
        'image_numbers': image_numbers,
    }

    df = pd.DataFrame(eval_data)

    results_dir = 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    save_path = os.path.join(results_dir, save_name)
    df.to_csv(save_path, index=False)
    print(f'Saved data to {save_path}')
