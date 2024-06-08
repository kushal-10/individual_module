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
DATA_DIR = os.path.join('llavadata', LEVEL)
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
            prompt = f"<image>\nYou are an intelligent agent playing a pentomino game. You are given a board with 20 x 20 grids and a target piece. Your spawn location is represented by the black circle on the board. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the {colour} {shape} shaped piece located on {position} of the board. Only respond in one word what next step will you take from ['left', 'right', 'up', 'down', 'grip']" 


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

        SAVE_PATH = os.path.join(DATA_DIR, f"{LEVEL}_{split}.json")
        generate_utils.save_as_json(split_data, SAVE_PATH)
        print(f"Data saved for split - {split} at {SAVE_PATH}")



if __name__=='__main__':
    llava_data()


'''
Command for LLaVA repo


deepspeed llava/train/train_mem.py \
    --lora_enable True --lora_r 128 --lora_alpha 256 --mm_projector_lr 2e-5 \
    --deepspeed ./scripts/zero3.json \
    --model_name_or_path liuhaotian/llava-v1.5-13b \
    --version v1 \
    --data_path ./playground/data/llava_v1_5_mix665k.json \
    --image_folder ./playground/data \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --mm_projector_type mlp2x_gelu \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end False \
    --mm_use_im_patch_token False \
    --image_aspect_ratio pad \
    --group_by_modality_length True \
    --bf16 True \
    --output_dir ./checkpoints/llava-v1.5-13b-task-lora \
    --num_train_epochs 1 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 50000 \
    --save_total_limit 1 \
    --learning_rate 2e-4 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --dataloader_num_workers 4 \
    --lazy_preprocess True \
    --report_to wandb   

Working Version:
deepspeed llava/train/train_mem.py \
    --lora_enable True --lora_r 128 --lora_alpha 256 --mm_projector_lr 2e-5 \
    --deepspeed ./scripts/zero3.json \
    --model_name_or_path liuhaotian/llava-v1.5-13b \
    --version v1 \
    --data_path ./playground/data/easy_train.json \
    --image_folder ./playground/data \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --mm_projector_type mlp2x_gelu \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end False \
    --mm_use_im_patch_token False \
    --image_aspect_ratio pad \
    --group_by_modality_length True \
    --bf16 True \
    --output_dir ./checkpoints/llava-v1.5-13b-task-lora \
    --num_train_epochs 1 \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 50000 \
    --save_total_limit 1 \
    --learning_rate 2e-4 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --tf32 False \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --dataloader_num_workers 1 \
    --lazy_preprocess True 

On A

'''