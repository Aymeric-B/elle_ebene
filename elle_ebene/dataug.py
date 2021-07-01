"""https://machinelearningmastery.com/how-to-develop-a-convolutional-neural-network-to-classify-photos-of-dogs-and-cats/"""

from PIL import Image
from elle_ebene.simple_preprocessing import to_numpy_rgb
from elle_ebene.simple_preprocessing import squared_imgs
from elle_ebene.simple_preprocessing import get_images
from keras.preprocessing.image import ImageDataGenerator


# Home directory
home_path = r'/Users/Mygenety/code/Aymeric-B/elle_ebene/raw_data/'
path = "/Users/Mygenety/code/Aymeric-B/elle_ebene/raw_data"

# Variables
batch_size = 15

# Preprocessing image 
type3_imgs = get_images("Type 3", path=path)
type4_imgs = get_images("Type 4/Hydratés", path=path)

type3_imgs_rgb = to_numpy_rgb(type3_imgs)
type4_imgs_rgb = to_numpy_rgb(type4_imgs)

type3_imgs_squared = squared_imgs(type3_imgs_rgb)
type4_imgs_squared = squared_imgs(type4_imgs_rgb)

def data_aug(model):
#Generate batches of tensor image data with real-time data augmentation.
#The data will be looped over (in batches so the size should be choosen in according to dataset size)
    datagen = ImageDataGenerator(
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='constant',
        cval = 255.,
        shuffle = False,
        validation_split = 0.2,     #Fraction of images reserved for validation
        brightness_range=[0.6,1.8]) 
    
    valid_datagen = ImageDataGenerator(validation_split = 0.2)

# ImageDataGenerator flow_from_directory pulls files one after another from a specific directory
    train_generator = datagen.flow_from_directory(
        directory=home_path + r'/train', # get images from train folder
        color_mode="rgb", 
        batch_size=batch_size,  # number of images to extract from folder for every batch
        class_mode="binary",    # classes to predict
        subset = "training")     # uses the validation split from datagen ^


    validation_generator = valid_datagen.flow_from_directory(
        directory=home_path + r'/train', # same directory as training data
        color_mode="rgb", 
        batch_size=batch_size,
        class_mode='binary',
        subset='validation') # set as validation data
    return train_generator, validation_generator
# After you have created and configured your ImageDataGenerator, you must fit it on your data. 
# This will calculate any statistics required to actually perform the transforms to your image data. 
# You can do this by calling the fit() function on the data generator and pass it your training dataset.






