# Cursor Detection and Motion Analysis

This project is a comprehensive toolkit for cursor detection and motion analysis, designed for providing semantic analysis for online recordings such as lecture recordings.

## Repository Structure:
- `cursor_detection`: contains dataset generation and YOLOv8 model training scripts
- `cursor-tracker`: contains functions to run, track and visualise cursor
- `motion_analysis`: contains scripts for performing semantic analysis on cursor movements
- `demo`: contains a sample result of trained model and motion analysis

```
cursor-motion-analysis/
├── cursor-detection/
│   └── dataset_generation.py
├── cursor-tracker/
│   └── to indicate/
│       ├── file
│       ├── and
│       ├── folder
│       └── nesting.
├── data/
│   ├── cursors
│   ├── generated/
│   │   └── **SAMPLE**/
│   │       ├── all
│   │       ├── train
│   │       ├── test
│   │       └── val
│   ├── images_raw/
│   │   └── **SAMPLE**
│   └── videos
├── .gitignore
├── README.md
└── requirements.txt
```

## Getting Started

1. Download requirements
2. Ensure directory same as above
3. Generate your own data given any slideshow and cursor images by running `dataset_generation.py`, then `train.py`
4. Given a video recording, save it into local `data` folder, then run `cursor_tracker/run.py`
- results will be saved into `results` folder
5. To perform motion_analysis, first retrieve info from detection
6. preprocess, then run the function to get all info! 