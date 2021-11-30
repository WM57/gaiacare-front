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

@app.post("/predict_grad_cam")
def predict_grad_cam(Img: Image):
    #decode image
    decoded = base64.b64decode(bytes(Img.image, 'utf-8'))
    decoded = np.frombuffer(decoded, dtype='uint8')
    decoded = decoded.reshape(Img.height, Img.width, Img.channel)

    #predict
    predictor = Predict()
    prediction = predictor.predict_grad_cam(decoded)
    predicted_class = predictor.predict_class(decoded)

    #switch to U-Int 8
    test_pic_array = prediction.astype('float32')

    #memorizing shape
    height, width, channel = test_pic_array.shape

    #reshape
    test_pic_array = test_pic_array.reshape(height * width * channel)

    # encoding to b64
    b64bytes = base64.b64encode(test_pic_array)
    #decoding to utf8 and turning to  string
    b64str = b64bytes.decode('utf8').replace("'", '"')

    image_dict = {
        'image': b64str,
        'height': height,
        'width': width,
        'channel': channel,
        'class': predicted_class
    }
    return image_dict
