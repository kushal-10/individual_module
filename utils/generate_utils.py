# Helper functions for generate.py

from PIL import Image
import json
import os

def save_as_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

def load_json(file_name):
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
    return data

def save_board_images(img_dir, rendered_image, prefix):
    if rendered_image is not None:
        generated_image = Image.fromarray(rendered_image)
        generated_image = generated_image.transpose(Image.FLIP_LEFT_RIGHT)  # Mirror horizontally
        generated_image = generated_image.transpose(Image.ROTATE_90)  # Rotate 90 degrees clockwise
        generated_image.save(os.path.join(img_dir, f'{prefix}.png'))
    else:
        print(f"Failed to render image")

def generate_initial_re(grid_info):
    piece_region = grid_info[0]['piece_region']
    piece_colour = grid_info[0]['piece_colour']
    piece_shape = grid_info[0]['piece_shape']
    return f"take the {piece_colour} {piece_shape} on {piece_region}"

def generate_steps_dict(steps):
    ACTION_TO_DIR = {0: "down", 1: "right", 2: "up", 3: "left"}
    return {f"step_{n}": ACTION_TO_DIR[step_value] for n, step_value in enumerate(steps)}
