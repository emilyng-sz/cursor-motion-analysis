# Functions should be used after motion analysis to visualise meaningful sections of the video

def overlay_points_on_frame(video_path, start_time, end_time, time_coord_data, pre_processed:bool=True, height=1280, width=1920, colour='white', time_ms = None):
    '''
    Overlays the points between start and end time according to time_coord_data
    if time_coord_raw is taken in, ensure pre_processed is False, so y / height is not inverted for plotting!

    Video frame chosen is the average of start and end time. Can also be specified by time_ms
    '''
    import cv2
    import matplotlib.pyplot as plt
    
    if time_ms is None:
        time_ms = (start_time+end_time)//2 

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, time_ms)
    _, frame = cap.read()
    frame = cv2.resize(frame, (width,height))
    plt.imshow(frame[:,:,::-1])
    
    x, y = zip(*list(map(lambda x: x[1], filter(lambda tup: tup[0] >= start_time and tup[0] <= end_time, time_coord_data))))
    if pre_processed: 
        plt.scatter(x,list(map(lambda x: height-x , y)), color=colour,marker='o')
    else:
        plt.scatter(x,list(map(lambda x: x , y)), color=colour,marker='o')

    plt.title(f"Cursor detected from {start_time}ms to {end_time}ms")

def get_loop_bounding_box(loop_info, time_coord_data, video_path, width = 1920, height = 1280, colour = (0, 1, 0)):
    '''
    takes in loop_info, time_coord_data and video_path to return cropped frame with bounding box and points of loop shown
    '''
    import matplotlib.pyplot as plt
    import math
    import cv2
    start_time = loop_info['start_time']
    end_time = loop_info['end_time']
    bounding_box = loop_info['bounding_box']
    time_ms = (start_time + end_time)//2
    width, height = 1920, 1280
    coords = list(map(lambda x: x[1], filter(lambda tup: tup[0] >= start_time and tup[0] <= end_time, time_coord_data)))
    x, y = zip(*coords)
    # Create a scatter plot of the original points
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, time_ms)
    _, frame = cap.read()
    frame = cv2.resize(frame, (width,height))
    plt.scatter(x, y, color=colour, label='Points')
    min_x, max_x, min_y, max_y = bounding_box['min_x'], bounding_box['max_x'], bounding_box['min_y'], bounding_box['max_y']
    plt.imshow(frame[math.floor(height-max_y):math.ceil(height-min_y),math.floor(min_x):math.ceil(max_x),::-1], 
            extent=(math.floor(min_x), math.ceil(max_x), math.floor(min_y), math.ceil(max_y)))
    plt.plot([min_x, max_x, max_x, min_x, min_x], [min_y, min_y, max_y, max_y, min_y], 
            color=colour, linestyle='--', linewidth=2, label='Bounding Box')
    plt.title(f"Loop from {start_time}ms to {end_time}ms")
