from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration
from prompts import UA_PROMPTS

#Load Image
path = "images/image.png"
image = Image.open(path).convert("RGB")

# Load Model
model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf")
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")

for p in list(UA_PROMPTS.keys()):
    prompt = UA_PROMPTS[p]

    # Process image + prompt
    inputs = processor(text=prompt, images=image, return_tensors="pt")

    # Generate
    generate_ids = model.generate(**inputs, max_length=256)
    response = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    print(response)