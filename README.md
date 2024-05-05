# CoGRIP

## General Information

    ├── agents                    
    │   ├── manhattan.py        # Manhattan path finder
    │   ├── llava15.py          # Llava1.5 as follower
    |   └── ...
    ├── dataset                 
    │   ├── level1.py           # Generate Level 1 dataset
    |   └── ... 
    ├── images                 
    ├── MCGrip                 
    │   ├── definitions.py      # Colour Definitions
    │   ├── environment.py      # Gym Environment class
    │   ├── layout.py           # Board Layout specifications
    │   ├── pieces.py           # Pieces Definitions + Basic Calculations                     
    └── ...

## Usage

### Base Setup
For Linux (Ubuntu 22.04)- 
```python
git clone https://github.com/kushal-10/individual_module.git
cd individual_module.git
export PYTHONPATH=.:$PYTHONPATH
pip install -r requirements.txt
```

Use ``` $env:PYTHONPATH = ".;DRIVE:\...\individual_module" ``` if using Windows.

### Generate instances

```python
python3 dataset/generate.py
```

Use this to generate 60 instances of Initial RE, Steps to reach the goal using Manhattan and Images of the board after each step



