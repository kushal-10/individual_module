
'''
1) Use the adapters to do inference on an image
- Try AutoAdapterModel loading for llava1.5
2) Set up evaluation pipeline
3) Use the adapters, base model and generate two results
'''

import torch
from transformers import AutoModelForVision2Seq

import os

import torch
from transformers import BertTokenizer
from adapters import BertAdapterModel

# Load pre-trained BERT tokenizer from Hugging Face
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# An input sentence
sentence = "It's also, clearly, great fun."

# Tokenize the input sentence and create a PyTorch input tensor
input_data = tokenizer(sentence, return_tensors="pt")

# Load pre-trained BERT model from Hugging Face Hub
# The `BertAdapterModel` class is specifically designed for working with adapters
# It can be used with different prediction heads
model = BertAdapterModel.from_pretrained('bert-base-uncased')