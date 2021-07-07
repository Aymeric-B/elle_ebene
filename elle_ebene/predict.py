#predict.py

from elle_ebene.baseline_model import initialize_model_base
from elle_ebene.model1 import initialize_model_1
from elle_ebene.utils.simple_preprocessing import resize_img, to_numpy_rgb, squared_imgs, normalize
from elle_ebene.hair_segmentation.hair_seg import HairSegmenter
from elle_ebene.params import RESIZING_DIM, MODEL_USED
import numpy as np
import os

predictor = None

class Predict():
    def __init__(self):
        """
            model_type = nom du modèle choisi, par défault 'baseline'
        """
        self.pipeline = None
        self.segmenter = None

    def model_init(self, path = os.path.join("model_weights", MODEL_USED, "weights")):
        """
        Initialize the model
        by default path = relative path for the website
        """
        weights_path = os.path.join(path)
        if MODEL_USED == "baseline":
            self.pipeline = initialize_model_base()
        elif MODEL_USED == "seg_aug":
            self.pipeline = initialize_model_1()

        self.pipeline.load_weights(weights_path)

        self.segmenter = HairSegmenter()
        self.segmenter.model_init()


    def predict(self, imgs):
        """
        prends en entrée une image ou liste d'images sous format PIL Image
        """
        if isinstance(imgs, list):
            clean_image = np.asarray(squared_imgs(to_numpy_rgb([resize_img(img, RESIZING_DIM) for img in imgs])))
            segmented_images = np.asarray(self.segmenter.get_hairs(clean_image))
            normalized_images = normalize(segmented_images)
            prediction = np.argmax(self.pipeline.predict(normalized_images), axis = 1)
        else : 
            clean_image = np.asarray(squared_imgs(to_numpy_rgb([resize_img(imgs, RESIZING_DIM)])))
            segmented_images = np.asarray(self.segmenter.get_hairs(clean_image))
            normalized_images = normalize(segmented_images)            
            prediction = np.argmax(self.pipeline.predict(normalized_images), axis = -1)[0]
        return prediction

def prediction(img):
    
    global predictor
    
    if predictor == None:
        predictor = Predict()
        predictor.model_init()
        print
    
    return predictor.predict(img)
    