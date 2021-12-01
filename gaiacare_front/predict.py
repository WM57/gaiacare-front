from tensorflow.keras import Input, Model, models
from tensorflow import argmax, GradientTape, reduce_mean
from tensorflow.keras.utils import array_to_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
import pandas as pd
import numpy as np
import matplotlib.cm as cm

class Predict():
    def __init__(self,
                 model = 'gaiacare_front/models/solution1_800-1000_no_datagen',
                 class_index = 'gaiacare_front/models/class.csv'):

        self.model = models.load_model(model)
        self.class_index = pd.read_csv(class_index).set_index('index').to_dict()['class']

    def predict_class(self, img_array):
        preproc_img = preprocess_input(img_array)
        class_name = list(self.class_index.keys())
        class_number = list(self.class_index.values())
        batch_img = np.expand_dims(preproc_img, axis=0)
        pred = self.model.predict(batch_img)

        return class_name[class_number.index(np.argmax(pred))]

    def predict_grad_cam(self, img_array):
        preproc_img = preprocess_input(img_array)

        # Setting up a model that returns the last convolutional output
        last_conv_layer = self.model.layers[0].get_layer('block5_conv3')
        classifier_layer_names = ["avg_pool", "predictions"]
        last_conv_layer_model = Model(self.model.layers[0].inputs, last_conv_layer.output)

        # Reapplying the classifier on top of the last convolutional output
        classifier_input = Input(shape=last_conv_layer.output.shape[1:])
        x = classifier_input
        x = self.model.layers[0].get_layer('block5_pool')(x)
        for layer_name in classifier_layer_names:
            x = self.model.get_layer(layer_name)(x)
        classifier_model =  Model(classifier_input, x)

        # Retrieving the gradients of the top predicted class
        with GradientTape() as tape:
            last_conv_layer_output = last_conv_layer_model(np.expand_dims(preproc_img, axis=0))
            tape.watch(last_conv_layer_output)
            preds = classifier_model(last_conv_layer_output)
            top_pred_index = argmax(preds[0])
            top_class_channel = preds[:, top_pred_index]

        grads = tape.gradient(top_class_channel, last_conv_layer_output)

        # Gradient pooling and channel-importance weighting
        pooled_grads = reduce_mean(grads, axis=(0, 1, 2)).numpy()
        last_conv_layer_output = last_conv_layer_output.numpy()[0]

        for i in range(pooled_grads.shape[-1]):
            last_conv_layer_output[:, :, i] *= pooled_grads[i]

        # Heatmap post-processing
        heatmap = np.mean(last_conv_layer_output, axis=-1)
        heatmap = np.maximum(heatmap, 0)
        heatmap /= np.max(heatmap)
        
        #remove below .5
        heatmap_zero = np.where(heatmap < 0.5)
        heatmap[heatmap_zero] = 0
        
        heatmap = np.uint8(255 * heatmap)

        jet = cm.get_cmap("Reds")
        jet_colors = jet(np.arange(256))[:, :3]
        jet_heatmap = jet_colors[heatmap]

        jet_heatmap = array_to_img(jet_heatmap)
        jet_heatmap = jet_heatmap.resize((img_array.shape[1], img_array.shape[0]))
        jet_heatmap = img_to_array(jet_heatmap)

        superimposed_array_img = jet_heatmap * 1 + img_array

        return superimposed_array_img
