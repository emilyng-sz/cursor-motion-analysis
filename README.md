# Cursor Detection and Motion Analysis

This project is a comprehensive toolkit for cursor detection and motion analysis, designed for providing semantic analysis for online recordings such as lecture recordings.

## Repository Structure:
- `cursor_detection`: contains dataset generation and YOLOv8 model training scripts
- `cursor-tracker`: contains functions to run, track and visualise cursor
- `motion_analysis`: contains scripts for performing semantic analysis on cursor movements
- `demo.ipynb`: contains a notebook to use and visualise results of trained model and motion analysis

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
   git clone <link>
   ```
2. Download all the required dependencies.
   ```sh
   pip install -r requirements.txt
   ```
3. Ensure directory is the same as above, and add any slide images to `images_raw` and populate `cursors` with desired cursor images to detect.
4. Generate your own data given any slideshow and cursor images by running `cursor_detection/dataset_generation.py`, then `cursor_detection/train.py`
5. Given a video recording, save it into local `data/videos` folder, then run `cursor_tracker/run.py`
- results will be saved into `results` folder
6. To perform motion_analysis, retrieve stored json data from `results`
7. Follow flow of `demo.ipynb` to retrieve all_info as your final result.