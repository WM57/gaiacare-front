from tensorflow.keras import models
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
import pandas as pd
import numpy as np


class Predict():
    def __init__(self,
                 model='gaiacare-front/models/solution1_800-1000_no_datagen',
                 class_index='gaiacare-front/models/class.csv'):
        #self.image = np.expand_dims(self.load_and_preprocess_image(image_path), axis=0)
        self.model = models.load_model(model)
        self.class_index = pd.read_csv(class_index).set_index(
            'index').to_dict()['class']

    def load_and_preprocess_image(self, image_path):
        img = load_img(image_path, target_size=[256, 256])
        array = img_to_array(img)
        return preprocess_input(array)

    def predict_class(self, image_path):
        img = load_img(image_path, target_size=[256, 256])
        array = img_to_array(img)
        preproc_img = preprocess_input(array)

        return list(self.class_index.keys())[list(
            self.class_index.values()).index(
                np.argmax(
                    self.model.predict(np.expand_dims(preproc_img, axis=0))))]


if __name__ == "__main__":

    pred = Predict()

    print(pred.predict_class('gaiacare-front/tests/test.JPG'))
