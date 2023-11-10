# Cursor Detection and Motion Analysis

Welcome to the Cursor Detection and Motion Analysis Toolkit, a comprehensive solution for cursor detection and motion analysis, designed for providing semantic analysis for online recordings such as lecture recordings.


## Key Features:

Cursor Detection: Accurate detection of cursor movements within recorded content.
- `cursor_detection` contains dataset generation and YOLOv8 model training scripts.
Cursor Tracker: Applies model and detects cursors on each frame of a recording.
- `cursor_tracker` contains functions to run, track and visualise the cursor.
Motion Insights: Analysis and categorisation of cursor trajectories and interactions.
- `motion_analysis` contains scripts for semantic analysis and categorisation of cursor moving in a loop, underline or stationary.

An exploratory Jupyter Notebook `demo.ipynb` is included for visualisation and explorations

## Repository Structure:

```
cursor-motion-analysis/
├── cursor_detection/
├── cursor_tracker/
├── motion_analysis/
├── demo.ipynb
├── .gitignore
├── README.md
├── requirements.txt
### Below files are untracked. Please ensure your repository has the same tree structure
├── data/
│   ├── cursors/
│   ├── generated/
│   │   └── **SAMPLE**/
│   │       ├── all
│   │       ├── train
│   │       ├── test
│   │       └── val
│   ├── images_raw/
│   │   └── **SAMPLE**/
│   └── videos/
├── weights/
└── results/
```

## Getting Started

1. Clone the repo.
   ```sh
   git clone https://github.com/emilyng-sz/cursor-motion-analysis.git
   ```
2. Download all the required dependencies.
   ```sh
   pip install -r requirements.txt
   ```
3. Ensure directory is the same as above, and upload images/recordings to the respective data folders (`images_raw`, `cursors`, `videos`)
4. Generate your own data by running `cursor_detection/dataset_generation.py`, then `cursor_detection/train.py`
6. Track a cursor on a video by running `cursor_tracker/run.py`
- results will be saved into `results` folder
7. To perform motion_analysis, retrieve stored json data from `results`
8. Follow instructions in `demo.ipynb` to retrieve all_info as your final result of semantic information
