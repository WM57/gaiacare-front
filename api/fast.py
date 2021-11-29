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


'''@app.post("/uploadfile/")
async def root(file: UploadFile = File(...)):
    with open(f'{file.filename}',"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    return '''


@app.post("/uploadfile")
async def create_upload_file(file: bytes = File(...)):

    #print("\nreceived file:")
    #print(type(file))
    #print(file)

    #image_path = "image_api.png"
    predictor = Predict(file, model)

    # write file to disk
    #with open(image_path, "wb") as f:
    #f.write(file)

    predictor.decode_image(224, 224)  # for VGG specs!
    result = predictor.get_prediction()

    movements = {
        predictor.class_names[i]: result[0][i]
        for i in range(len(result[0]))
    }
    print(type(movements))
    # main_movement =  predictor.class_names[np.argmax(result[0])]
    # model -> pred
    # dict(pred=str(main_movement))

    return dict(pred=str(movements))
