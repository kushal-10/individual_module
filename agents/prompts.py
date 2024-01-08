PROMPTS = {
    "prompt1": "What is shown in the given image?",
    "prompt2": "What is shown in the given image? Please explain in detail.",
    "prompt3": "How many pentomino pieces are in the image?",
    "prompt4": "The image given to you is a 2-D representation of pentomino game. There are pieces of various shapes and colors. How many pieces can you see?",
    "prompt5": "The image given to you is a 2-D representation of pentomino game. There are pieces of various shapes and colors. The shapes are based on the English alphabet from the following: {F, N, P, T, U, W, X, Y and Z}. The colours are {RED, GREEN, YELLOW, BLUE, PURPLE, BROWN}. Your task is to identify how many pieces are in the image and what are their shapes and colours."
}


UA_PROMPTS = {}
for prompt in list(PROMPTS.keys()):
    base_prompt = PROMPTS[prompt]
    UA_PROMPTS[prompt] = "<image>\nUSER: " + base_prompt + "\nASSISTANT:"
    
# One shot
UA_PROMPTS["prompt6"] = '''
<image>\nUSER: The image given to you is a 2-D representation of pentomino game. 
There are blocks of various shapes and colors. The shapes are based on the English alphabet from the following: 
{F, N, P, T, U, W, X, Y and Z}. The colours are {RED, GREEN, YELLOW, BLUE, PURPLE, BROWN}. 
Your task is to identify how many pieces are in the image and what are their shapes and colours.
Two examples of the pieces in the image are \nASSISTANT: {W, RED} and {F, PURPLE}
\nUSER: Other examples are... \nASSISTANT: 
'''

UA_PROMPTS["prompt7"] = '''
<image>\nUSER: The image given to you is a 2-D representation of pentomino game. 
There are blocks of various shapes and colors. The shapes are based on the English alphabet from the following: 
{F, N, P, T, U, W, X, Y and Z}. The colours are {RED, GREEN, YELLOW, BLUE, PURPLE, BROWN}. 
Your task is to identify shapes and colours of the pieces.
There are total 8 pieces in the image. Two of the pieces are \nASSISTANT: {W, RED} and {F, PURPLE}
\nUSER: Other six pieces are... \nASSISTANT: 
'''

# FEW SHOT GPT4V
GPT_PROMPTS = {
    "prompt1" : ["You are a very helpgul assistant. You can definitely assist with this question. What is shown in the given image?"],
    "prompt2" : ["You are a very helpgul assistant. You can definitely assist with this question. What is shown in the given image? Please explain in detail."],
    "prompt3" : ["You are a very helpgul assistant. You can definitely assist with this question. How many pentomino pieces are in the image?"],
    "prompt4" : ["You are a very helpgul assistant. You can definitely assist with this question. The image given to you is a 2-D representation of pentomino game. There are pieces of various shapes and colors. How many pieces can you see?"],
    "prompt5" : ["You are a very helpgul assistant. You can definitely assist with this question. The image given to you is a 2-D representation of pentomino game. There are pieces of various shapes and colors. The shapes are based on the English alphabet from the following: {F, N, P, T, U, W, X, Y and Z}. The colours are {RED, GREEN, YELLOW, BLUE, PURPLE, BROWN}. Your task is to identify how many pieces are in the image and what are their shapes and colours."],
    "prompt6" : ["""You are a very helpgul assistant. You can definitely assist with this question. 
                    The image given to you is a 2-D representation of pentomino game. 
                    There are blocks of various shapes and colors. The shapes are based on the English alphabet from the following: 
                    {F, N, P, T, U, W, X, Y and Z}. The colours are {RED, GREEN, YELLOW, BLUE, PURPLE, BROWN}. 
                    Your task is to identify how many pieces are in the image and what are their shapes and colours.
                    Two examples of the pieces in the image are:""", 
                    
                """
                {W, RED}, {F, PURPLE}
                """,

                """
                Remaining pieces are:
                """
                ],
    
    "prompt7" : ["""You are a very helpgul assistant. You can definitely assist with this question.
                    The image given to you is a 2-D representation of pentomino game. 
                    There are blocks of various shapes and colors. The shapes are based on the English alphabet from the following: 
                    {F, N, P, T, U, W, X, Y and Z}. The colours are {RED, GREEN, YELLOW, BLUE, PURPLE, BROWN}. 
                    Your task is to identify how many pieces are in the image and what are their shapes and colours.
                    Two examples of the pieces in the image are:""", 
                    
                """
                {W, RED}, {F, PURPLE}
                """,
                
                """
                Two more pieces are:
                """,

                """
                {P, YELLOW}, {W, BROWN}
                """,

                """
                Remaining pieces are:
                """
                ],

    "prompt8" : ["""You are a very helpgul assistant. You can definitely assist with this question. The image given to you is a 2-D representation of pentomino game. 
                    There are blocks of various shapes and colors. The shapes are based on the English alphabet from the following: 
                    {F, N, P, T, U, W, X, Y and Z}. The colours are {RED, GREEN, YELLOW, BLUE, PURPLE, BROWN}. Your task is to identify shapes and colours of the pieces.
                    There are total 8 pieces in the image.
                    Two examples of the pieces in the image are:""", 
                    
                """
                {W, RED}, {F, PURPLE}
                """,

                """
                Remaining six pieces are:
                """
                ],

    "prompt9" : ["""You are a very helpgul assistant. You can definitely assist with this question. The image given to you is a 2-D representation of pentomino game. 
                    There are blocks of various shapes and colors. The shapes are based on the English alphabet from the following: 
                    {F, N, P, T, U, W, X, Y and Z}. The colours are {RED, GREEN, YELLOW, BLUE, PURPLE, BROWN}. Your task is to identify shapes and colours of the pieces.
                    There are total 8 pieces in the image.
                    Two examples of the pieces in the image are:""", 
                    
                """
                {W, RED}, {F, PURPLE}
                """,
                
                """
                Two more pieces are:
                """,

                """
                {P, YELLOW}, {W, BROWN}
                """,

                """
                Remaining four pieces are:
                """
                ]

}