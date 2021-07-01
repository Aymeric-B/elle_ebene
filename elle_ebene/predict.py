
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

    def model_init(self):
        """
        Initialize the model
        """
        if self.model_type == "baseline":
            self.pipeline = initialize_model()
            self.pipeline.load_weights("model_weights/baseline/weights")


    def predict(self, img):
        """
        prends en entrée une image sous format PIL Image
        """

        clean_image = normalize(np.asarray(squared_imgs(to_numpy_rgb([resize_img(img, RESIZING_DIM)]))))
        prediction = np.argmax(self.pipeline.predict(clean_image), axis = -1)[0]

        return prediction