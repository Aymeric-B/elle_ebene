import pandas as pd
import joblib

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

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2


@app.get("/")
def index():
    return dict(Greeting="Bonjour les cheveux texturés !")


@app.get("/predict")
def predict(image1, image2, image3):
    
        # pipeline = get_model_from_gcp()
    pipeline = joblib.load('model.joblib')

    # make prediction
    result1 = pipeline.predict(image1)
    result2 = pipeline.predict(image2)
    result3 = pipeline.predict(image3)