# CoGRIP

## Structure

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

## Usage

### Base Setup
For Linux (Ubuntu 22.04)- 

1) Setup main repo

```python
git clone https://github.com/kushal-10/individual_module.git
cd individual_module
export PYTHONPATH=.:$PYTHONPATH
pip install -r requirements.txt
```

Use ``` $env:PYTHONPATH = ".;DRIVE:\...\individual_module" ``` if using Windows.

2) Clone LLaVA repo under the root folder where ```individual_module``` is cloned
   
```python
git clone https://github.com/haotian-liu/LLaVA.git
```

    ├── root_folder                    
    │   ├── individual_module           # This repo
    |   └── LLaVA                       # LLaVA repo
    └── ...

Refer to further setup instructions mentioned on their repo - [LLaVA](https://github.com/haotian-liu/LLaVA)

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


### LLaVA Dataset 
After generating the instances (steps + initial_re + images), convert that data into LLaVA compatible format by running

```python
python3 instances/create_llava_data.py 
```
