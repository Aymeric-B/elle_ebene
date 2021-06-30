import pandas as pd
import numpy as np
import joblib

from elle_ebene.simple_preprocessing import resize_img, to_numpy_rgb, squared_imgs
from elle_ebene.params import RESIZING_DIM

import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return dict(Greeting="Bonjour les cheveux texturés !")


@app.get("/predict")
def predict(image):
    
    
    # pre-pre-processing
    resizing_dim = RESIZING_DIM
    image = resize_img(image, resizing_dim)
    images = to_numpy_rgb([image])
    image_squared = squared_imgs(images, fill_color = [255,255,255])
    image = np.asarray(image_squared)
    image = image / 255
    
    # pipeline = get_model_from_gcp()
    pipeline = joblib.load('model.joblib')

    # make prediction
    pred = np.argmax(pipeline.predict(image) , axis = -1)[0]

    # récupérer la prédiction de predict.py

    if pred == 1:
        type = "type 4"
    else:
        type = "type 3"
    
    return dict(prediction=type)
