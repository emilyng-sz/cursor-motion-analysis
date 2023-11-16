# About pre_trained_model_metrics

Metrics in this folder are based on a privately generated dataset which was also used to train the model found in `weights/`. 

There are 188 images in the test dataset

## Code 

Generates the images in this folder and statistics which are shown below.

*Disclaimer: as the data is private, the code is unable to access the files and will not run on your local environment.*


```
from ultralytics import YOLO
model = YOLO("runs/detect/train26/weights/best.pt")

# use the same data augmentation metrics as training
metrics = model.val(data='validate_test_dataset.yaml', rect=True, batch=8, epochs=10, plots=True,
                      close_mosaic = 0, mosaic=0, translate=0, fliplr=False, 
                      hsv_h = 0.3, hsv_s = 0.3, hsv_v = 0.3, scale = 0.0,
                      max_det = 1)
```

### metrics from accessing metrics.box

Average Precision (ap), with IoU threshold
- ap: 0.68117
- ap50: 0.96704

F1 score
- f1: 0.95231

Mean Average Precision (map), with IoU threshold
- map: 0.6811676627002917
- map50: 0.9670354184334928
- map75: 0.7703671586498878

Recall:
- mr: 0.93796537117117
