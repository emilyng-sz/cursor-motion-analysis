import cv2
import json

def generate_results(model, video_path:str, max_det_1 = True):
    video_name = video_path.split('/')[-1].split('.')[0]
    cap = cv2.VideoCapture(video_path)

    # Create a list to store detection results
    detections = []

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (1920,1280)) # width and height flipped

        # Perform object detection using YOLOv8
        results = model(frame)
        timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))

        if not max_det_1:
            for i in range(len(results[0].boxes.xyxy)):
                bboxes = results[0].boxes.xyxy[i].cpu().numpy()
                class_label = results[0].names[int(results[0].boxes.cls.numpy()[i])]
                confidences = float(results[0].boxes.conf.cpu().numpy()[i]) 

                # Prepare detection data for the frame
                x1, y1, x2, y2 = bboxes[0], bboxes[1], bboxes[2], bboxes[3]
                detection = {
                        'timestamp': timestamp,
                        'class_label': class_label,
                        'confidence': confidences[i],
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'bbox_tl': int(x1), 'bbox_bl': int(y1), 'bbox_tr': int(x2), 'bbox_br': int(y2),
                        'coordinates': coordinate,
                        'coord_x': coordinate[0], 'coord_y': coordinate[1]
                    }
                # Append frame detections to the list of detections
                detections.append(detection)

        # only take the best detection
        else:

            if len(results[0].boxes.cls) > 1: # multiple detections
                print(timestamp, 'with', len(results[0].boxes.cls) )

            confidences = list(map(float, results[0].boxes.conf.cpu().numpy()))

            if not confidences: # will have empty values
                print(timestamp , " has 0 cursors. Skipping...")
                continue

            # finds the best 
            best_index = confidences.index(max(confidences)) # chooses only result with best confidence
            bboxes = results[0].boxes.xyxy[best_index].cpu().numpy()
            x1, y1, x2, y2 = bboxes[0], bboxes[1], bboxes[2], bboxes[3]
            coordinate = ((x1+x2)/2, (y1+y2)/2)

            # loops through ALL detected cursors:
            for i in range(len(confidences)):
                bboxes = results[0].boxes.xyxy[i].cpu().numpy()
                x1, y1, x2, y2 = bboxes[0], bboxes[1], bboxes[2], bboxes[3]
                coordinate = ((x1+x2)/2, (y1+y2)/2)
                detection = {
                        'timestamp': timestamp,
                        'class_label': results[0].names[int(results[0].boxes.cls.numpy()[i])],
                        'confidence': confidences[i],
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'bbox_tl': int(x1), 'bbox_bl': int(y1), 'bbox_tr': int(x2), 'bbox_br': int(y2),
                        'coordinates': coordinate,
                        'coord_x': coordinate[0], 'coord_y': coordinate[1]
                    }
                detections.append(detection)

    # Save detections to a JSON file
    if not max_det_1:
        output_file = f'results/{video_name}_all_detections.json'
    else:
        output_file = f'results/{video_name}_max_detection.json'
    
    with open(output_file, 'w') as json_file:
        json.dump(detections, json_file, indent=4)

    print(f"Detections saved to {output_file}")

# define helper functions for cursor tracking
def convert_FPS(source_path:str, dest_path:str, desired_fps:int):
    '''
    converts video in source_path to desired_fps, and saves as dest_path 
    assumes source video is of mp4 format
    '''
    cap = cv2.VideoCapture(source_path)

    # Get the video properties
    frame_width = int(cap.get(3))  # Frame width
    frame_height = int(cap.get(4))  # Frame height
    original_fps = cap.get(5)  # Original FPS

    if int(original_fps) == desired_fps:
        print(f'Video is already at {desired_fps} FPS')
        return 

    # Create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec (codec may vary based on the file format)
    out = cv2.VideoWriter(dest_path, fourcc, desired_fps, (frame_width, frame_height))

    # Loop to read and write frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # No more frames to read
        # Write the frame to the output video
        out.write(frame)
    cap.release()
    out.release()

    print(f"Video converted successfully to {desired_fps} FPS")


if __name__ == '__main__':
    from ultralytics import YOLO
    model = YOLO("runs/detect/train26/weights/best.pt")
    video_path = "data/recordings/Youtube_section2.mp4"
    new_video_path = 'data/recordings/Youtube_section2_10fps.mp4'
    convert_FPS(video_path, new_video_path, 10)
    generate_results(model, new_video_path, max_det_1 = True)