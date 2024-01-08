
import base64

def create_message(prompts, image):
    '''
    Based on the given prompt/s create a message chain to feed into GPT4V
    Args:
        prompt - A list of prompts (len -> {1,3,5})
        images - A list of images (len -> {1,2,3})
    Returns:
        messages - A list of messages for GPT4V
    '''

    messages = []
    for i in range(len(prompts)):
        if i%2==0:
            messages.append({"role": "user", "content": [{"type": "text", "text": prompts[i]}, {"type": "image_url", "image_url": image}]})
        else:
            messages.append({"role": "assistant", "content": prompts[i]})


    return messages
    

# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
