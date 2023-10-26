from ultralytics import YOLO
model = YOLO("yolov8n.pt") 

# Train the model with specified parameters for the use-case of online lecture recordings with minimal variation
# Limited data preprocessing is required and most parameters are hence low/False
# Note that imgsize should NOT be specified (refer to https://github.com/ultralytics/ultralytics/issues/3955)
results = model.train(data="SAMPLE.yaml", rect=True, batch=8, epochs=10, plots=True,
                      close_mosaic = 0, mosaic=0, translate=0, fliplr=False, 
                      hsv_h = 0.3, hsv_s = 0.3, hsv_v = 0.3, scale = 0.0,
                      max_det = 1) 

# successful runs will output metrics and weights to a folder named 'runs/detect/trainX'