import pandas as pd
from PIL import Image
import os
import io
import progressbar
import pyarrow as pa
import pyarrow.parquet as pq

LEVEL = 'easy'

# Create save folder
SAVE_DIR = os.path.join('parquet_data', LEVEL)
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

    df = pd.read_json(file_path)
    print(type(df['messages'][0]))
 
    messages = []
    images = []

    bar = progressbar.ProgressBar(maxval=len(df)).start()
    for i in range(len(df)):
        if i<2:
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
    print(parquet_data)
    parquet_df = pd.DataFrame(parquet_data)
    table = pa.Table.from_pandas(parquet_df)
    pq.write_table(table, save_path)

    print(f"Saved parquet file for level - {LEVEL}, split - {split_name} at {save_path}")

    return None

    
if __name__=='__main__':

    level_name = 'easy'
    train_path = os.path.join('hf_data', level_name, 'train.json')
    test_path = os.path.join('hf_data', level_name, 'test.json')
    validation_path = os.path.join('hf_data', level_name, 'validation.json')

    create_parquet_file(validation_path)
    create_parquet_file(test_path)
    create_parquet_file(train_path)
