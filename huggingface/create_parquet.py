import pandas as pd
from PIL import Image
import os
import io
import progressbar

LEVEL = 'easy'

# Create save folder
SAVE_DIR = os.path.join('data', 'parquet_data', LEVEL)
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def create_parquet_file(file_path: str):
    '''
    Create parquet file following VSFT dataset 
    Ref - https://huggingface.co/datasets/HuggingFaceH4/llava-instruct-mix-vsft/viewer

    Args:
        file_path: csv file containing 'messages' and 'images' (file path), created by running hf_dataset.py
    '''

    # Save path 
    split_name = file_path.split('/')[-1].split('.')[0]
    save_path = os.path.join(SAVE_DIR, f'{split_name}.parquet')
    print(f"Creating parquet file for level - {LEVEL}, split - {split_name}")

    df = pd.read_csv(file_path)
 
    messages = []
    images = []

    bar = progressbar.ProgressBar(maxval=len(df)).start()
    for i in range(len(df)):

        msg = df['messages'][i]
        messages.append(msg)

        # Get image data in byte form
        img_path = df['images'][i]
        img = Image.open(img_path)
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        image_data = buffer.getvalue()

        # Create VSFT type list object
        img_list = [{'bytes': image_data, 'path': None}]
        images.append(img_list)
        bar.update(i)


    parquet_data = {
        'messages': messages,
        'images': images
    }

    
    parquet_df = pd.DataFrame(parquet_data)
    parquet_df.to_parquet(save_path, engine='pyarrow')
    print(f"Saved parquet file for level - {LEVEL}, split - {split_name} at {save_path}")

    return None

    
if __name__=='__main__':

    csv_dir = os.path.join('data', 'hf_data', LEVEL)
    train_path = os.path.join(csv_dir, 'train.csv')
    test_path = os.path.join(csv_dir, 'test.csv')
    validation_path = os.path.join(csv_dir, 'validation.csv')

    create_parquet_file(validation_path)
    create_parquet_file(test_path)
    create_parquet_file(train_path)