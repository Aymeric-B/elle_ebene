from predict import baseline

from PIL import Image

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from io import BytesIO

# from PIL import Image

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


# @app.get("/predict")
# def predict(image):
    
#     #image = Image.open(path)
    
#     # Call to predict function
#     pred = baseline(image)

#     # Traitement de la prédiction
#     if pred == 1:
#         type = "type 4"
#     else:
#         type = "type 3"
    
#     return dict(prediction=type)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = await file.read()
    
    return {"filetype": file.file.}
    
    # Call to predict function
    pred = baseline(image)
    

    # Traitement de la prédiction
    if pred == 1:
        type = "type 4"
    else:
        type = "type 3"
    
    return dict(prediction=type)
    