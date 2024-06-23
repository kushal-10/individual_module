'''
# Use this script to generate the dataset in the format mentioned in LLaVA Repo
# Ref - https://github.com/haotian-liu/LLaVA/blob/main/docs/Finetune_Custom_Data.md

[
  {
    "id": "997bb945-628d-4724-b370-b84de974a19f",
    "image": "part-000001/997bb945-628d-4724-b370-b84de974a19f.jpg",
    "conversations": [
      {
        "from": "human",
        "value": "<image>\nWrite a prompt for Stable Diffusion to generate this image."
      },
      {
        "from": "gpt",
        "value": "a beautiful painting of chernobyl by nekro, pascal blanche, john harris, greg rutkowski, sin jong hun, moebius, simon stalenhag. in style of cg art. ray tracing. cel shading. hyper detailed. realistic. ue 5. maya. octane render. "
      },
    ]
  },
]
'''

from utils import generate_utils

import os
import progressbar
import random



LEVEL = 'easy'
DATA_DIR = os.path.join('data', LEVEL)
SPLITS = os.listdir(DATA_DIR)

def llava_data():
    '''
    Saves a llava_data.json file, as specified for LLaVA
    '''
    for split in SPLITS:
        boards = os.listdir(os.path.join(DATA_DIR, split))
        print(f"Creating LLaVA data for split : {split}")

        split_data = []

        bar = progressbar.ProgressBar(maxval=len(boards)).start()
        for i, board in enumerate(boards):
            image_dir = os.path.join(DATA_DIR, split, board, 'images')
            text_dir = os.path.join(DATA_DIR, split, board, 'text')
            initial_re_json = generate_utils.load_json(os.path.join(text_dir, 'initial_re.json'))
            initial_re = initial_re_json['initial_re']

            # Create input prompt from initial RE
            re_split = initial_re.split()
            colour = re_split[2]
            shape = re_split[3]
            position = re_split[5]
            if len(re_split) == 7:
                position += ' ' + re_split[6]
            prompt = f"USER: <image>\nYou are given a board with 20 x 20 grids and a target piece. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your spawn location is represented by the black circle on the board and you can only move ['left', 'right', 'up', 'down'] - Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the {colour} {shape} shaped piece located on {position} of the board. Only respond in one word.\nASSISTANT:"

            for img in os.listdir(image_dir):
                image_name = img.split('.')[0]
                steps = generate_utils.load_json(os.path.join(text_dir, 'steps.json'))
                answer = steps[image_name]

                json_object = {
                    "id": split + "_" + board + "_" + image_name,
                    "image": os.path.join(image_dir, img),
                    "conversations": [
                        {
                            "from": "human",
                            "value": prompt
                        },
                        {
                            "from": "gpt",
                            "value": answer
                        }
                    ]
                }

                split_data.append(json_object)
            bar.update(i)

        random.shuffle(split_data)

        SAVE_PATH = os.path.join('data', 'ft_data', f"{LEVEL}_{split}_optimized_prompt.json")
        generate_utils.save_as_json(split_data, SAVE_PATH)
        print(f"Data saved for split - {split} at {SAVE_PATH}")



if __name__=='__main__':
    llava_data()
