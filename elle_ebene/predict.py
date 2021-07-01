
from elle_ebene.baseline_model import initialize_model
from elle_ebene.simple_preprocessing import resize_img, to_numpy_rgb, squared_imgs, normalize
from elle_ebene.params import RESIZING_DIM
import numpy as np

class Predict():
    def __init__(self, model_type = "baseline"):
        """
            model_type = nom du modèle choisi, par défault 'baseline'
        """
        self.pipeline = None
        self.model_type = model_type

    def model_init(self, path = "../model_weights/baseline/weights"):
        """
        Initialize the model
        by default path = relative path for the website
        """
        if self.model_type == "baseline":
            self.pipeline = initialize_model()
            self.pipeline.load_weights(path)


    def predict(self, imgs):
        """
        prends en entrée une image ou liste d'images sous format PIL Image
        """
        if isinstance(imgs, list):
            clean_image = normalize(np.asarray(squared_imgs(to_numpy_rgb([resize_img(img, RESIZING_DIM) for img in imgs]))))
            prediction = np.argmax(self.pipeline.predict(clean_image), axis = 1)
        else : 
            clean_image = normalize(np.asarray(squared_imgs(to_numpy_rgb([resize_img(imgs, RESIZING_DIM)]))))
            prediction = np.argmax(self.pipeline.predict(clean_image), axis = -1)[0]
        return prediction