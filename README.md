# Cursor Detection and Motion Analysis

This project is a comprehensive toolkit for cursor detection and motion analysis, designed for providing semantic analysis for online recordings such as lecture recordings.

## Repository Structure:
- `cursor_detection`: contains dataset generation and YOLOv8 model training scripts
- `motion_analysis`: contains scripts for tracking and analysing cursor movements
- `demo`: contains a sample result of trained model and motion analysis

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