
'''
1) Use the adapters to do inference on an image
- Try AutoAdapterModel loading for llava1.5
2) Set up evaluation pipeline
3) Use the adapters, base model and generate two results
'''

import torch
from transformers import AutoModelForVision2Seq, AutoTokenizer
from adapters import AutoAdapterModel

model_id = "llava-hf/llava-1.5-13b-hf"

model = AutoAdapterModel.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

print(model)