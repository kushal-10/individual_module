import os
from openai import OpenAI
client = OpenAI(
    api_key="")
from prompts import GPT_PROMPTS
from gptbackend import create_message

image_url = "https://raw.githubusercontent.com/kushal-10/individual_module/main/images/image.png?token=GHSAT0AAAAAACJDXXNXJWQMRZJSWYCSD7KSZM4CS6A"

prompts = list(GPT_PROMPTS.keys())

for p in prompts:
    message = create_message(GPT_PROMPTS[p], image_url)
    print("Prompt: ")
    print(GPT_PROMPTS[p])
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=message,
        max_tokens=300,
    )
    print("Response: ")
    print(response.choices[0].message.content)
