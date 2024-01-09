import os
import tensorflow as tf
from tensorflow import _keras_module
from keras.models import load_model
import cv2
import imghdr
import numpy as np
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.metrics import Precision, Recall, BinaryAccuracy


## TESTING AND SAVING MODEL

img = cv2.imread('kroos.jpg')
#plt.imshow(img)
#plt.show()

resize = tf.image.resize(img, (256,256))
#plt.imshow(resize.numpy().astype(int))
#plt.show()


new_model = load_model(os.path.join('models', 'skinToneClassifier.h5'))
new_model.predict(np.expand_dims(resize/255, 0))

yhat = new_model.predict(np.expand_dims(resize/255, 0))
print(yhat)
maxVal = np.max(yhat[0])
print(maxVal)

# Access each probability individually and convert to regular float
c1 = float(yhat[0][0])
c2 = float(yhat[0][1])
c3 = float(yhat[0][2])
c4 = float(yhat[0][3])
c5 = float(yhat[0][4])
c6 = float(yhat[0][5])
c7 = float(yhat[0][6])
c8 = float(yhat[0][7])
c9 = float(yhat[0][8])
c10 = float(yhat[0][9])

skinToneCodes = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

for code in skinToneCodes:
    if code == maxVal:
        print("Skin type is of code " + str(skinToneCodes.index(code)+1))
        break