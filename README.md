# CoGRIP

## I Structure

    ├── agents                    
    │   ├── manhattan.py           # Manhattan path finder
    |   └── ...
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
    └── ...

## II Usage

### A) Base Setup
For Linux (Ubuntu 22.04)- 

1) Setup main repo

```python
git clone https://github.com/kushal-10/individual_module.git
cd individual_module
export PYTHONPATH=.:$PYTHONPATH
pip install -r requirements.txt
```

a) Use ``` $env:PYTHONPATH = ".;DRIVE:\...\individual_module" ``` if using Windows.

b) If there is an error while installing packages; the following usually works; and then, if required, reinstall missing packages
```python
pip install --upgrade setuptools wheel
pip cache purge
```
2) Clone LLaVA repo under the root folder where ```individual_module``` is cloned
   
```python
git clone https://github.com/haotian-liu/LLaVA.git
```

    ├── root_folder                    
    │   ├── individual_module           # This repo
    |   └── LLaVA                       # LLaVA repo
    └── ...

Refer to further setup instructions mentioned on their repo - [LLaVA](https://github.com/haotian-liu/LLaVA)

### B) Create splits

```python
python3 instances/create_splits.py
```

Use this to Generate a dataset of 2880 instances (60% train, 20% test, 20% validation). This creates 10 board setting fro each combination of 6 Colours, 6 Shapes and 8 Positions.

### C) Generate instances

```python
python3 instances/generate_instances.py
```

This generates the gameplay for each board setting in the previous step, used for offline RL. The boards are setup here, along with the initial RE. The steps are calculated using Manhattan pathfinder, the gameplay is simulated via gym environment. The dataset is saved in 
```data``` folder.


### D) LLaVA Dataset 
After generating the instances (steps + initial_re + images), convert that data into LLaVA compatible format by running

Follow the convention mentioned in - [Finetune Llava](https://github.com/haotian-liu/LLaVA/blob/main/docs/Finetune_Custom_Data.md)
```python
python3 instances/create_llava_data.py 
```

### E) Train an adapter
After generating the LLaVA dataset, use the script provided by the authors to train an adapter available here - [finetune_task_lora.sh](https://github.com/haotian-liu/LLaVA/blob/main/scripts/v1_5/finetune_task_lora.sh)

The exact command used here for fine-tuning is available under ```instances/finetune.sh```. Be sure, to check the dataset JSON file is in an appropriate location and modify its path accordingly

This needs to be run under the LLaVA repository, Checkout their [README](https://github.com/haotian-liu/LLaVA?tab=readme-ov-file) for more information on how to proceed
