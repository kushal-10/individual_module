from jinja2 import Template

def apply_llava_template(message: str):
    '''
    Apply Llava Chat template

    Args:
        message: A string of the format prompt+" Answer:"+answer
    Returns:    
        chat_message: meeage with proper chat template 
    '''
    
    splits = message.split("ANSWER:")
    user_prompt = splits[0].strip()
    assistant_resp = splits[1].strip()
    messages = [
        {'role': 'user', 'content': user_prompt},
        {'role': 'assistant', 'content': assistant_resp}
    ]

    LLAVA_TEMPLATE = "{%- for message in messages -%}{% if message['role'] == 'user' %}\nUSER: <image>\n{{message['content']}}{% elif message['role'] == 'assistant' %}\nASSISTANT:{{message['content']}}{% endif %}{% endfor %}"
    template = Template(LLAVA_TEMPLATE)
    chat_message = template.render(messages=messages)
    
    return chat_message

if __name__=='__main__':
    apply_llava_template("")