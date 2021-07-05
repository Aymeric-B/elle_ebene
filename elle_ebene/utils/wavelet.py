import pywt
import numpy as np
import matplotlib.pyplot as plt



def mean(chan_list, coef):
    return np.expand_dims(np.mean(np.stack([chan_list[i][coef] for i in range(3)], axis = -1), axis = 2),axis = -1)

def apply_filter(image, kind="coif17"):
    chan_3 = []
    for i in range(3):
        coeffs2 = pywt.dwt2(image[:,:,i], kind)
        ll, (lh, hl, hh) = coeffs2
        chan_3.append((ll.astype("uint8"), lh.astype("uint8"), hl.astype("uint8"), hh.astype("uint8")))
    A = 255-mean(chan_3, 0)
    H = 255-mean(chan_3, 1)
    V = 255-mean(chan_3, 2)
    D = 255-mean(chan_3, 3)
    list_transforms = [A,H,V,D]
    return list_transforms

def rotate_numpy_image(img):
    new_img = np.empty(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[j,img.shape[1]-1-i] = img[i,j]
    return new_img

def mean_imgs(list_imgs):
    return np.mean(np.stack(list_imgs, axis = -1), axis = 2)

def apply_filter_grey(kind, image):
    ll, (lh, hl, hh)  = pywt.dwt2(image, kind)
    LL = ll
    LH = 255-lh
    HL = 255-hl
    HH = 255-hh
    return LL, LH, HL, HH

def cumul_rot(img):
    rotations_list = [img]
    for i in range(3):
        rotations_list.append(rotate_numpy_image(rotations_list[-1]))
    return mean_imgs(rotations_list)