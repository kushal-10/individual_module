from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration
import torch
from PIL import Image
import requests
from prompts import UA_PROMPTS

path = "images/image.png"
image = Image.open(path).convert("RGB")

processor = InstructBlipProcessor.from_pretrained("Salesforce/instructblip-vicuna-7b")
model = InstructBlipForConditionalGeneration.from_pretrained("Salesforce/instructblip-vicuna-7b", load_in_4bit=True, torch_dtype=torch.float16)

for p in list(UA_PROMPTS.keys()):
    prompt = UA_PROMPTS[p]

    inputs = processor(images=image, text=prompt, return_tensors="pt").to(device="cuda", dtype=torch.float16)

    # autoregressively generate an answer
    outputs = model.generate(
            **inputs,
            num_beams=5,
            max_new_tokens=512,
            min_length=1,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.5,
            length_penalty=1.0,
            temperature=1,
    )
    outputs[outputs == 0] = 2 
    generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
    print(prompt)
    print(generated_text)

