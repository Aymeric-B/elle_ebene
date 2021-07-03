"""
Contient les fonctions permettant de la segmentation de cheveux - fonctionne mal sur les photos de dos
On n'utilise pas dlib
"""

from tensorflow.keras import models
import numpy as np

from elle_ebene.hair_segmentation.hairnet import get_model

class HairSegmenter():
    def __init__(self):
        """
            model_type = nom du modèle choisi, par défault 'baseline'
        """
        self.model = None
        

    def model_init(self, path = "raw_data/hair_seg/weights"):
        """
        Initialize the model
        by default path = relative path for the website
        """
        self.model = get_model()
        self.model.load_weights(path)

    def get_hair_from_mask(self, mask, image):
        """
        à partir d'un masque et d'une image, on récupère uniquement les pixels correspondant au masque
        """
        mask[mask > 0.5] = 255
        mask[mask <= 0.5] = 0

        idx=(mask==0)
        hair = image.copy()
        hair[idx]=[255,255,255]
        return hair

    def predict_PIL(self, image, height=224, width=224):
        im = image.copy()
        im = im / 255
        im = im.reshape((1,) + im.shape)

        pred = self.model.predict(im)

        mask = pred.reshape((224, 224))

        return mask

    def get_hairs(self, imgs_list):
        """
        à partir d'une liste d'images on récupère une liste filtrée avec les cheveux
        """
        hairs = []
        for image in imgs_list:
            mask = self.predict_PIL(image)
            hair = self.get_hair_from_mask(mask, image)
            hairs.append(hair)
        return hairs
