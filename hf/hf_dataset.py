# Create dataset in VSFT format - Message + Image location for now
# Ref - https://huggingface.co/datasets/HuggingFaceH4/llava-instruct-mix-vsft/viewer
# Run this script after creating the splits of the dataset (instances/generate_instances.py)
import os
import progressbar
import pandas as pd

from utils.generate_utils import load_json

SPLITS = ['train', 'test', 'validation']
LEVELS = ['easy']
DATA = 'data'

# Check for folders
def check_directories_exist():
    for level in LEVELS:
        for split in SPLITS:
            path = os.path.join(DATA, level, split)
            if not os.path.exists(path):
                raise FileNotFoundError(f"The directory '{path}' does not exist. Please make sure it is created.")

'''
[ 
    { "content": 
        [{ "index": null, "text": prompt "type": "text" }, 
         { "index": 0, "text": null, "type": "image" } ], "role": "user" }, 
    { "content": 
        [{ "index": null, "text": "Donna Eden", "type": "text" } ], "role": "assistant" }, 
]
'''


def create_messages(initial_re: str, answer: str):
    '''
    Create the prompt based on the initial RE
    Args:
        inital_re - Initial Referring Expression for the episode
        answer - Answer for each turn - (left, right, up, down or grip)
    Return:
        messages - A list of messages compatible with vsft 
    '''

    re_split = initial_re.split()
    colour = re_split[2]
    shape = re_split[3]
    position = re_split[5]
    if len(re_split) == 7:
        position += ' ' + re_split[6]
    prompt = f"Your are an intelligent agent playing a pentomino game. You are given a board with 20 x 20 grids and a target piece. Your spawn location is represented by the black circle on the board. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the {colour} {shape} shaped piece located on {position} of the board. Only respond in one word what next step will you take from ['left', 'right', 'up', 'down', 'grip']" 

    message = prompt + " ANSWER:" + answer
    return message


def generate_csvs():
    '''
    Generate and save csv files for each leve/split containing messages + images
    '''

    for level in LEVELS:
        for split in SPLITS:
            split_path = os.path.join(DATA, level, split)
            boards = os.listdir(split_path)
            boards.sort()

            MESSAGES = []
            IMAGES = []
            print(f"Setting up prompts for level: {level}, split {split}")
            bar = progressbar.ProgressBar(maxval=len(boards)).start()
            for i, board_path in enumerate(boards):
                # Load Initial RE and steps
                re_csv = load_json(os.path.join(split_path, board_path, 'text', 'initial_re.json'))
                initial_re = re_csv['initial_re']
                steps_path = os.path.join(split_path, board_path, 'text', 'steps.json')
                steps = load_json(steps_path)

                for s in steps.keys():
                    answer = steps[s]
                    message = create_messages(initial_re, answer)
                    image_path = str(os.path.join(split_path, board_path, 'images', str(s)+'.png'))
                    MESSAGES.append(message)
                    IMAGES.append(image_path)
                
                bar.update(i)

            SAVE_DIR = os.path.join('hf_data', level)
            if not os.path.exists(SAVE_DIR):
                os.makedirs(SAVE_DIR)
            SAVE_PATH = os.path.join(SAVE_DIR, f'{split}.csv')
            data = {
                'messages': MESSAGES,
                'images': IMAGES
            }
            df = pd.DataFrame(data)
            df.to_csv(SAVE_PATH, index=False)

if __name__ == '__main__':
    # Check if the dataset and splits are created.
    try:
        check_directories_exist()
        print("All necessary directories exist.")
    except FileNotFoundError as e:
        print(e)

    generate_csvs()

    # # Check csvs
    # df1 = pd.read_csv('hf_data/easy/train.csv')
    # df2 = pd.read_csv('hf_data/easy/test.csv')
    # df3 = pd.read_csv('hf_data/easy/validation.csv')
    # #16142, 5406, 5358
    # print(len(df1), len(df2), len(df3))


    

    

