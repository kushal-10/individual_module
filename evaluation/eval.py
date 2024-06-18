"""
TODOS - 1806
1) Use the adapters to do inference on an image
- Try AutoAdapterModel loading for llava1.5
2) Set up evaluation pipeline
3) Use the adapters, base model and generate two results

Main cli command for inference

Working (sort of) cli, but try CG solution
python run_llava.py --model-path /LLaVA/llava/checkpoints/llava-v1.5-13b-task-lora/adapter_model \
--model-base ../../../llava-1.5-13b-hf \
--image-file /LLaVA/playground/data/llavadata/easy/test/board_0/images/step_0.png \
--query "<image>\nYou are an intelligent agent playing a pentomino game. You are given a board with 20 x 20 grids and a target piece. Your spawn location is represented by the black circle on the board. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the red P shaped piece located on top left of the board. Only respond in one word what next step will you take from ['left', 'right', 'up', 'down', 'grip']"
"""

from transformers import AutoModelForVision2Seq, AutoProcessor
from peft import PeftModel

# Load base model
# model_name = "../llava-1.5-13b-hf"
model_name = "llava-hf/llava-1.5-13b-hf"
base_model = AutoModelForVision2Seq.from_pretrained(model_name)

# Load fine-tuned adapter
adapter_path = "../LLaVA/checkpoints/llava-v1.5-13b-task-lora"  # Replace with your adapter path
model = PeftModel.from_pretrained(base_model, adapter_path)

print(model)




