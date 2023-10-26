from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import shutil
import glob

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

# overlay cursor images
generate_data("../data", "slide_img_for_TESTING", "cursors")
# split train test split
train, validation, test = 0.6, 0.2, 0.2
train_test_val_split("../data", "slide_img_for_TESTING_nc1", train, validation, test)

