"""https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-to-classify-photos-of-dogs-and-cats/"""

import os
from elle_ebene.utils.simple_preprocessing import to_numpy_rgb, squared_imgs, get_images
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# Home directory
home_path = r'/Users/Mygenety/code/Aymeric-B/elle_ebene/raw_data/Data'
path_pic = '/Users/Mygenety/code/Aymeric-B/elle_ebene/raw_data/Data_aug'
# Variables
batch_size = 64

# Preprocessing image 
type3_imgs = get_images("Type 3", path=home_path)
type4_imgs = get_images("Type 4", path=home_path)

type3_imgs_rgb = to_numpy_rgb(type3_imgs)
type4_imgs_rgb = to_numpy_rgb(type4_imgs)

type3_imgs_squared = squared_imgs(type3_imgs_rgb)
type4_imgs_squared = squared_imgs(type4_imgs_rgb)

def data_gen(path_pic, batch_size, model):
#Generate batches of tensor image data with real-time data augmentation.
#The data will be looped over (in batches so the size should be choosen in according to dataset size)
    train_path = os.path.join(path_pic,'train')
    val_path = os.path.join(path_pic,'val')
    
# Data augmentation to training data   
    datagen = ImageDataGenerator(
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='constant',
        cval = 255.,
        brightness_range=[0.6,1.8]) 
# No data augmentation to validation data   
    valid_datagen = ImageDataGenerator()

# ImageDataGenerator flow_from_directory pulls files one after another from a specific directory
    train_generator = datagen.flow_from_directory(
        directory=train_path, 
        color_mode="rgb", 
        batch_size=batch_size,  # number of images to extract from folder for every batch
        class_mode="binary",
        save_to_dir= r'/Users/Mygenety/code/Aymeric-B/elle_ebene/raw_data/augmented')    # keep if you want to store images
    
    train_generator.next()
    
    validation_generator = valid_datagen.flow_from_directory(
        directory=val_path, 
        color_mode="rgb", 
        batch_size=batch_size,
        class_mode='binary')

# training the model   
    total_images = train_generator.n  
    steps = total_images//batch_size    
    
    model.fit_generator(  #vs a .fit because we have data augmentation
        train_generator,
        steps_per_epoch=steps, # where is the train data?
        epochs=50,
        validation_data=validation_generator,
        validation_steps=800)
    
    return train_generator, validation_generator
# After you have created and configured your ImageDataGenerator, you must fit it on your data. 
# This will calculate any statistics required to actually perform the transforms to your image data. 
# You can do this by calling the fit() function on the data generator and pass it your training dataset.

    # #count the files   
    # def folder_count(directory):
    #     APP_FOLDER = directory
    #     #totalFiles =0
    #     for base, dirs, files in os.walk(APP_FOLDER):
    #         files = 0
    #         #totalDir = 0
    #         print('Searching in: ', base)
    #         print('Number of directories:' , dirs)
    #         for Files in files:
    #             files +=1
    #             #totalFiles += 1
    #         print('Total number of files', files)
    #     return  files
    
    # batch_size=folder_count(train_path)
    # print(batch_size)
 
   


