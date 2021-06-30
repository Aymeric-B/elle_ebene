
from elle_ebene.baseline_model import initialize_model
from elle_ebene.simple_preprocessing import resize_img, to_numpy_rgb, squared_imgs, normalize
from elle_ebene.params import RESIZING_DIM
import numpy as np

def baseline(img):
    """
    prends en entrée une image sous format PIL Image
    """
    model = initialize_model()
    model.load_weights("/home/aymeric/code/Aymeric-B/elle_ebene/model_weights/baseline/weights")

    clean_image = normalize(np.asarray(squared_imgs(to_numpy_rgb([resize_img(img, RESIZING_DIM)]))))
    prediction = np.argmax(model.predict(clean_image), axis = -1)[0]

    return prediction