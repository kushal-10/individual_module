# Helper functions for generate.py

from PIL import Image
import json
import os

# Constants
SAVE_DIR = 'data'
TRANSPOSE_TRANSFORMS = [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90]

def save_as_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

def save_board_images(img_dir, image_array, prefix):
    for idx, image in enumerate(image_array):
        if image is not None:
            for transform in TRANSPOSE_TRANSFORMS:
                transformed_image = Image.fromarray(image).transpose(transform)
                transformed_image.save(os.path.join(img_dir, f'{prefix}_{idx + 1}.png'))
        else:
            print(f"Failed to render {prefix} {idx + 1}")

def generate_initial_re(grid_info):
    piece_region = grid_info[0]['piece_region']
    piece_colour = grid_info[0]['piece_colour']
    piece_symbol = grid_info[0]['piece_symbol']
    return f"take the {piece_colour} {piece_symbol} on {piece_region}"

def generate_steps_dict(steps):
    ACTION_TO_DIR = {0: "down", 1: "right", 2: "up", 3: "left"}
    return {f"step_{n}": ACTION_TO_DIR[step_value] for n, step_value in enumerate(steps)}
