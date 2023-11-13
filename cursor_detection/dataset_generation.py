from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import shutil
import glob
import pyautogui
import cv2

def generate_data(data_path:str, img_folder:str, cursor_folder:str, 
                  save_with_category = True,
                  img_w_h = (1920, 1080), cursor_h_range = (25, 38)):
    '''
    Takes in path to data folder, background images and cursor images to overlap;
          specify background image width and height to resize into, specify a range of cursor heights to resize
    
    For each image in img_folder, overlays a random cursor and saves new image with model results it into data_path/generated/img_folder
    '''
    # Open slide image
    slide_names = os.listdir(os.path.join(data_path, "images_raw", img_folder))
    cursor_names = os.listdir(os.path.join(data_path, cursor_folder))
    if ".DS_Store" in cursor_names: cursor_names.remove(".DS_Store")
    num_cursors = len(cursor_names)-1
    print(f"Number of cursor images: {num_cursors} from path {os.path.join(data_path, cursor_folder)}")

    for slide_name in slide_names:

        # Open and Rezie slide image
        slide = Image.open(os.path.join(data_path, "images_raw", img_folder, slide_name))
        slide = slide.resize(size=img_w_h)
    
        # Open one cursor image randomly
        rand_index = np.random.randint(0, num_cursors)
        cursor_name = cursor_names[rand_index]
        if "pointer" in cursor_name:
            category = 0
        elif "hand" in cursor_name:
            category = 1 
        elif "text" in cursor_name:
            category = 2
        else:
            raise ValueError(f"Uncategorised cursor image: {cursor_name}")
        
        cursor = Image.open(os.path.join(data_path, cursor_folder, cursor_name))

        # Resize cursor image
        cursor_w, cursor_h = cursor.size  
        slide_w, slide_h = img_w_h # equivalent to slide.size
        desired_height = np.random.randint(cursor_h_range[0], cursor_h_range[1])
        scaling_f = (desired_height / cursor_h)
        resize_w, resize_h = int(scaling_f * cursor_w), int(scaling_f * cursor_h)
        cursor = cursor.resize(size=(resize_w, resize_h))
        
        # Overlay cursor image on slide
        x, y = np.random.randint(0, slide_w-resize_w), np.random.randint(0, slide_h-resize_h)
        slide.paste(cursor, (x, y), mask=cursor)

        # Save Result for One pointer category i.e. num_category = 1
        generated_raw_path = os.path.join(data_path, "generated", img_folder + "_nc1")
        if not os.path.exists(generated_raw_path):
            os.mkdir(generated_raw_path)
        if not os.path.exists(generated_raw_path+"/all"):
            os.mkdir(generated_raw_path+"/all")
        slide.save(os.path.join(generated_raw_path, "all", slide_name))
        # Create annotation file
        f = open(os.path.join(generated_raw_path, "all", slide_name.split('.')[0] + ".txt"), "w")
        f.write(f"0 {(x+(0.5*resize_w))/slide_w} {(y+(0.5*resize_h))/slide_h} {resize_w/slide_w} {resize_h/slide_h}")
        f.close()  
        
        if save_with_category:
            generated_raw_path = os.path.join(data_path, "generated", img_folder + "_nc3")
            if not os.path.exists(generated_raw_path):
                os.mkdir(generated_raw_path)
            if not os.path.exists(generated_raw_path+"/all"):
                os.mkdir(generated_raw_path+"/all")
            slide.save(os.path.join(generated_raw_path, "all", slide_name))
            # Create annotation file
            f = open(os.path.join(generated_raw_path, "all", slide_name.split('.')[0] + ".txt"), "w")
            f.write(f"{category} {(x+(0.5*resize_w))/slide_w} {(y+(0.5*resize_h))/slide_h} {resize_w/slide_w} {resize_h/slide_h}")
            f.close()  

def train_test_val_split(data_path:str, img_folder:str, train, validation, test):
    generated_img_folder = os.path.join(data_path, "generated", img_folder)
    # path to destination folders
    train_folder = os.path.join(generated_img_folder, 'train')
    val_folder = os.path.join(generated_img_folder, 'val')
    test_folder = os.path.join(generated_img_folder, 'test')

    random.seed(42)

    file_names = os.listdir(generated_img_folder+'/all')
    random.shuffle(file_names)

    train_size = int(len(file_names) * train)
    val_size = int(len(file_names) * validation)
    test_size = int(len(file_names) * test)

    # Create destination folders if they don't exist
    for folder_path in [train_folder, val_folder, test_folder]:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Copy image files to destination folders
    for i, file_name in enumerate(file_names):
        if i < train_size:
            dest_folder = 'train'
        elif i < train_size + val_size:
            dest_folder = 'val'
        else:
            dest_folder = 'test'
        raw_name = '*'+file_name.split('.')[0]
        if '[' in raw_name:
            raw_name = raw_name.split(']')[1]
        
        # should check if files are .jpg or .png
        shutil.copy(glob.glob(generated_img_folder+'/all/'+raw_name+'*.jpg')[0], os.path.join(generated_img_folder, dest_folder, file_name.split('.')[0]+".png"))
        shutil.copy(glob.glob(generated_img_folder+'/all/'+raw_name+'*.txt')[0], os.path.join(generated_img_folder, dest_folder, file_name.split('.')[0]+".txt"))

def generate_cursor_video(output_vid_name, desired_width = 1920, desired_height = 1280, fps=10, duration_sec = 5, cursor_file_name = 'pointer8.png'):
    '''
    Screen records the cursor movement for input duration
    Pastes a specified cursor image of height 25 on the screen (with transparency) 
    Outputs video and log file of cursor coordinates in data/videos

    Transparency overlay code referecned from: https://gist.github.com/clungzta/b57163b165d3247af2ebfe2868f7dccf
    LIMITTAION: please do not hover cursor too near the right and bottom edges of the screen as cursor will be out of bounds
    '''

    video_path = os.path.join('data', 'videos', output_vid_name + '.mp4')
    log_path = os.path.join('data', 'videos', output_vid_name + '.txt')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    scree_width, screen_height = pyautogui.size()
    out = cv2.VideoWriter(video_path, fourcc, fps, (desired_width, desired_height))
    log_file = open(log_path, "w")
    increment = 1000/fps
    count = 0
    while True:
        # Capture screen content
        frame = pyautogui.screenshot()
        x, y = pyautogui.position() # top left corner of cursor

        x,y = int(x*(desired_width/scree_width)), int(y*(desired_height/screen_height))
        log_file.write(f"{round(count*increment)},{x},{y}\n")
        count += 1

        frame = np.array(frame)
        # Convert BGR format (used by OpenCV) to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (desired_width, desired_height))

        ### Load cursor image to be pasted
        cursor = Image.open(f'data/cursors/{cursor_file_name}')
        # Resize cursor image
        cursor_w, cursor_h = cursor.size  
        scaling_f = (25 / cursor_h) # 25 is the desired height of the cursor
        resize_w, resize_h = int(scaling_f * cursor_w), int(scaling_f * cursor_h)
        cursor = cursor.resize(size=(resize_w, resize_h))
        cursor = np.array(cursor)

        # seprate alpha value of cursor png to retain transparency
        b,g,r,a = cv2.split(cursor)
        overlay_color = cv2.merge((b,g,r))
        h, w, _ = overlay_color.shape
        mask = cv2.medianBlur(a,5)
        roi = frame[y:y+h, x:x+w]
        # frame[y:min(y + cursor_h,desired_height), x:min(x + cursor_w,desired_width)] = cursor[0:min(cursor_h,desired_height-y), 0:min(cursor_w,desired_width-x)]
        # x, y = int(x-(float(w)/2.0)), int((y-float(h)/2.0))
        
        # Black-out the area behind the logo in our original ROI
        img1_bg = cv2.bitwise_and(roi,roi,mask = cv2.bitwise_not(mask))
        
        # Mask out the logo from the logo image.
        img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)

        # Update the original image with our new ROI
        frame[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

        out.write(frame)
        
        if count*increment > duration_sec*1000: 
            break
    
    out.release()
    cv2.destroyAllWindows()
    log_file.close()

    print(f"Video saved to {video_path}")
    print(f"Cursor positions saved to {log_path}")

if __name__ == '__main__':
    # overlay cursor images
    generate_data("../data", "slide_img_for_TESTING", "cursors")
    # split train test split
    train, validation, test = 0.6, 0.2, 0.2
    train_test_val_split("../data", "slide_img_for_TESTING_nc1", train, validation, test)

