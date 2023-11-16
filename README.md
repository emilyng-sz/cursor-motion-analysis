# Cursor Detection and Motion Analysis

Welcome to the Cursor Detection and Motion Analysis Toolkit, a comprehensive solution for cursor detection and motion analysis, designed for providing semantic analysis for online recordings such as lecture recordings.


## Key Features:

Cursor Detection: Accurate detection of cursor movements within recorded content.
- `cursor_detection` contains dataset generation and YOLOv8 model training scripts.
Cursor Tracker: Applies model and detects cursors on each frame of a recording.
- `cursor_tracker` contains functions to run, track and visualise the cursor.
Motion Insights: Analysis and categorisation of cursor trajectories and interactions.
- `motion_analysis` contains scripts for semantic analysis and categorisation of cursor moving in a loop, underline or stationary.
- `pretrained_model_metrics` contains evaluation metrics for pretrained model

An exploratory Jupyter Notebook `demo.ipynb` is included for visualisation and explorations

## Repository Structure:
- `cursor_detection`: contains dataset generation and YOLOv8 model training scripts
- `cursor-tracker`: contains functions to run, track and visualise cursor
- `motion_analysis`: contains scripts for performing semantic analysis on cursor movements
- `model_demo.ipynb`: contains scripts to generate cursor recordings as ground truth and test model accuracy
- `motion_analysis_demo.ipynb`: contains a notebook to use and visualise results of trained model and motion analysis

```
cursor-motion-analysis/
├── cursor_detection/
├── cursor_tracker/
├── motion_analysis/
├── pretrained_model_metrics/
├── model_demo.ipynb
├── motion_analysis_demo.ipynb
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
3. Ensure directory is the same as above, and add any folder of slide images to `images_raw` and populate `cursors` with desired cursor images to detect.
4. Generate your own data given any slideshow and cursor images by running `cursor_detection/dataset_generation.py`, then `cursor_detection/train.py`
5. Given a video recording, save it into local `data/videos` folder, then run `cursor_tracker/run.py`
- results will be saved into `results` folder
6. To perform motion_analysis, retrieve stored json data from `results`
7. Follow steps in `motion_analysis_demo.ipynb` to retrieve all_info as your final result.

- Feel free to explore the various helper functions available!
- To use pre-trained weights, access them through the google drive link [here](https://drive.google.com/file/d/1slDiZoA8iIYpuUpWtbFqfv3R5VF14Zn-/view?usp=sharing)