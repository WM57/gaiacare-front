from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import base64
import numpy as np

from pydantic import BaseModel
from gaiacare_front.predict import Predict

class Image(BaseModel):
    image: str
    height: int
    width: int
    channel: int

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def home():
    return {"greeting": "Welcome to GaiaCare API"}

@app.post("/predict")
def predict_class(Img: Image):
    #decode image
    decoded = base64.b64decode(bytes(Img.image, 'utf-8'))
    decoded = np.frombuffer(decoded, dtype='uint8')
    decoded = decoded.reshape(Img.height, Img.width, Img.channel)
    #predict class
    predictor = Predict()
    prediction = predictor.predict_class(decoded)
    print(prediction)
    return prediction
