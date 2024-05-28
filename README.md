# CoGRIP

## Structure
    ├──------------------------------------------------------------------------------------------
    ├── agents                    
    │   ├── manhattan.py           # Manhattan path finder
    |   └── ...
    ├── huggingface                
    │   ├── tune_llava.py          # Fine tuning script for llava-hf models
    │   ├── template.py            # Script to apply Jinja template
    │   ├── hf_dataset.py          
    │   ├── create_parquet.py      # Generate parquet data for Huggingface 
    ├── instances                 
    │   ├── create_splits.py       # Generate Easy level splits
    |   └── generate_instances.py  # Setup the images, InitialRE and simulate the instances                  
    ├── MCGrip                 
    │   ├── definitions.py         # Colour Definitions
    │   ├── environment.py         # Gym Environment class
    │   ├── layout.py              # Board Layout specifications
    │   ├── pieces.py              # Pieces Definitions + Basic Calculations
    ├── splits                 
    │   ├── easy                  
    │   │   ├── metadata.json      # Contains instance distribution across splits     
    ├── utils                      # Various utility functions
    │   ├── generate_utils.py         
    │   ├── layout_utils.py                    
    └──-------------------------------------------------------------------------------------------

## Usage

### Base Setup
For Linux (Ubuntu 22.04)- 

```python
git clone https://github.com/kushal-10/individual_module.git
cd individual_module
export PYTHONPATH=.:$PYTHONPATH
pip install -r requirements.txt
```

Use ``` $env:PYTHONPATH = ".;DRIVE:\...\individual_module" ``` if using Windows.

### Create splits

```python
python3 instances/create_splits.py
```

Use this to Generate a dataset of 2880 instances (60% train, 20% test, 20% validation). This creates 10 board setting fro each combination of 6 Colours, 6 Shapes and 8 Positions.

### Generate instances

```python
python3 instances/generate_instances.py
```

This generates the gameplay for each board setting in the previous step, used for offline RL. The boards are setup here, along with the initial RE. The steps are calculated using Manhattan pathfinder, the gameplay is simulated via gym environment. The dataset is saved in 
```data``` folder.


### HF dataset

The dataset used here is already available as a Huggingface dataset and can be directly used from the datasets library to start the instruction tuning.

However to replicate the dataset creation; run the following commands

1) Creates the csv files containing messages and image paths
```python
python3 huggingface/hf_dataset.py 
```

2) Converts the messages and image paths to parquet objects for each split
```python
python3 huggingface/create_parquet.py
```

### LLaVA Dataset (Deprecated)
Check mode/llava_github branch