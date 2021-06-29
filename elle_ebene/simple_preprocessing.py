"""
Ce fichier doit contenir toutes les fonctions de preprocessing 'simple' des images:
- lire toutes les images quel que soit leur format (png, jpg, jpeg)
- passer toutes les images en rgb
- mettre toutes les photos à la même dimension
- padder les photos avec une couleur prédéfinie
- générer un dataset mélangé avec des lables
"""

from elle_ebene.params import RESIZING_DIM
import os
from PIL import Image
import numpy as np


def resize_img(img, resizing_dim):
    """
    resize the image to a maximum dimension on height and width keeping the aspect ratio
    """
    width, height = img.size
    if height > width:
        ratio = resizing_dim /height
        new_width  = int(ratio * width)
        img_ = img.resize((new_width, resizing_dim), Image.ANTIALIAS)
    else:
        ratio = resizing_dim /width
        new_height  = int(ratio * height)
        img_ = img.resize((resizing_dim, new_height), Image.ANTIALIAS)
    return img_

def get_images(folder_name, resizing_dim = RESIZING_DIM, valid_images = [".jpg",".jpeg",".png"], path = "/home/aymeric/code/Aymeric-B/elle_ebene/raw_data"):
    """
    Give the folder name (in raw_data) to get all images from this folder.
    """
    path_ = os.path.join(path, folder_name)
    imgs_list = []
    for file in os.listdir(path_):
        ext = os.path.splitext(file)[1]
        if ext.lower() not in valid_images:
            continue
        img = Image.open(os.path.join(path_,file))
        img_ = resize_img(img, resizing_dim)
        imgs_list.append(img_)
    return imgs_list

def to_numpy_rgb(list_imgs):
    """
    transforms the images in a list to rgb (just removes the alpha)
    transform the PIL image into a numpy array
    """
    imgs_rgb = []
    for img in list_imgs:
        imgs_rgb.append(np.array(img)[:,:,:3])
    return imgs_rgb

def squared_imgs(list_imgs, fill_color = COLOR_BACKGROUND):
    """
    transform a list of images of various sizes (but with a common max dimension) into sqaured images
    the backround is filled with the given color
    """
    imgs_squared = []
    resizing_dim = max(list_imgs[0].shape) # plutôt que d'avoir une variable, on prends la dimension max (entre largeur et hauteur) sur la première image

    for img in list_imgs:
        ht, wd, cc= img.shape

        # create new image of desired size and color (white) for padding
        ww = resizing_dim
        hh = resizing_dim
        result = np.full((hh,ww,cc), fill_color, dtype=np.uint8)

        # compute center offset
        xx = (ww - wd) // 2
        yy = (hh - ht) // 2

        # copy img image into center of result image
        result[yy:yy+ht, xx:xx+wd] = img
        imgs_squared.append(result)

    return imgs_squared

def create_dataset(list_list_imgs, list_arrays_labels):
    """
    create a dataset from a list of lists of images and a matching list of lists of labels
    """
    if len(list_list_imgs) != len(list_arrays_labels):
        return "error : not the same number of images lists and of labels lists"
    for i in range(len(list_list_imgs)):
        if len(list_list_imgs[i]) != len(list_arrays_labels[i]):
            return f"error : the lengths of the images list number {i} does not match the length of the labels list number {i}"
    
    list_arrays_imgs = [np.asarray(list_imgs) for list_imgs in list_list_imgs]
    concat_images = np.concatenate(tuple(list_arrays_imgs))
    concat_labels = np.concatenate(tuple(list_arrays_labels))
    X, y = unison_shuffled_copies(concat_images, concat_labels)
    return X, y

def unison_shuffled_copies(a, b):
    """
    shuffles two numpy arrays the same way
    """
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

def normalize(img):
    return img / 255