from elle_ebene.simple_preprocessing import get_images, to_numpy_rgb, squared_imgs, normalize
import numpy as np
from elle_ebene.simple_preprocessing import create_dataset
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

def get_data_locally():
    """
    returns X_train, X_test, y_train, y_test
    """
    # on récupère les photos
    abs_path = "/home/aymeric/code/Aymeric-B/elle_ebene/raw_data"
    type3_imgs = get_images("Type 3", path=abs_path)
    type4_imgs = get_images("Type 4", path=abs_path)

    type3_clean = clean_images(type3_imgs)
    type4_clean = clean_images(type4_imgs)

    type3_labels = np.full((len(type3_clean),),3)
    type4_labels = np.full((len(type4_clean),),4)

    X, y = create_dataset([type3_clean, type4_clean] , [type3_labels, type4_labels])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

    y_train = to_categorical(y_train,5)[:,-2:]
    y_test = to_categorical(y_test,5)[:,-2:]

    return X_train, X_test, y_train, y_test

def clean_images(imgs_list):
    """
    prend en entrée une liste d'images, renvoie la liste d'images à la même dimension, sous format numpy et normalisée
    """
    # on les passe en numpy et rgb
    imgs_rgb = to_numpy_rgb(imgs_list)
    # on les passe toutes au même format
    imgs_squared = squared_imgs(imgs_rgb)
    # on les normalise et on les passe en array  
    imgs_normalized = np.asarray([normalize(img) for img in imgs_squared])

    return imgs_normalized
