"""
TODOS - 1806
1) Use the adapters to do inference on an image
- Try AutoAdapterModel loading for llava1.5
2) Set up evaluation pipeline
3) Use the adapters, base model and generate two results
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


# import requests
from PIL import Image
#
import torch
# from transformers import AutoProcessor, LlavaForConditionalGeneration

model_id = "llava-hf/llava-1.5-13b-hf"

prompt = "<image>\nYou are an intelligent agent playing a pentomino game. You are given a board with 20 x 20 grids and a target piece. Your spawn location is represented by the black circle on the board. There are 3 more distractor pieces. These pieces resemble one of the letters from ['P', 'T', 'U', 'W', 'X', 'Z']. Your task is to take a step or grip the piece. The step should be towards the direction of the target piece. Proceed to take the red P shaped piece located on top left of the board. Only respond in one word what next step will you take from ['left', 'right', 'up', 'down', 'grip']\n ASSISTANT:"
image_file = "data/easy/test/board_0/images/step_0.png"

# model = LlavaForConditionalGeneration.from_pretrained(
#     model_id,
#     torch_dtype=torch.float16,
#     low_cpu_mem_usage=True,
# ).to(0)

processor = AutoProcessor.from_pretrained(model_id)

raw_image = Image.open(image_file).convert('RGB')
inputs = processor(prompt, raw_image, return_tensors='pt').to(0, torch.float16)

output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
print(processor.decode(output[0][2:], skip_special_tokens=True))





