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
from keras.utils import to_categorical
from sklearn.metrics import precision_score, recall_score, accuracy_score



## SETUP
# Avoid OOM errors by setting GPU Memory Consumption Growth
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus: 
    tf.config.experimental.set_memory_growth(gpu, True)
tf.config.list_physical_devices('GPU')


## DATA CLEANUP
data_dir = 'data' 
image_exts = ['jpeg','jpg', 'bmp', 'png']
for image_class in os.listdir(data_dir): 
    for image in os.listdir(os.path.join(data_dir, image_class)):
        image_path = os.path.join(data_dir, image_class, image)
        try: 
            img = cv2.imread(image_path)
            tip = imghdr.what(image_path)
            if tip not in image_exts: 
                print('Image not in ext list {}'.format(image_path))
                os.remove(image_path)
        except Exception as e: 
            print('Issue with image {}'.format(image_path))
            # os.remove(image_path)


## LOAD DATA
data = tf.keras.utils.image_dataset_from_directory('data')
data_iterator = data.as_numpy_iterator()
batch = data_iterator.next()
fig, ax = plt.subplots(ncols=4, figsize=(20,20))
for idx, img in enumerate(batch[0][:4]):
    ax[idx].imshow(img.astype(int))
    ax[idx].title.set_text(batch[1][idx])


## SCALE DATA
data = data.map(lambda x,y: (x/255, y))
scaled_iterator = data.as_numpy_iterator()
batch = scaled_iterator.next()
batch[0].max()


# SPLIT DATA
train_size = int(len(data) * 0.7)
val_size = int(len(data) * 0.2)
test_size = int(len(data) * 0.1)

temp_train = data.take(train_size)
temp_val = data.skip(train_size).take(val_size)
temp_test = data.skip(train_size + val_size).take(test_size)
test_labels = np.array(list(temp_test.map(lambda x, y: y)))
# Create datasets with both features and one-hot encoded labels
train_dataset = temp_train.map(lambda x, y: (x, tf.one_hot(y, depth=10)))
val_dataset = temp_val.map(lambda x, y: (x, tf.one_hot(y, depth=10)))
test_dataset = temp_test.map(lambda x, y: (x, tf.one_hot(y, depth=10)))

# BUILD MODEL
model = Sequential()
model.add(Conv2D(16, (3, 3), 1, activation='relu', input_shape=(256, 256, 3)))
model.add(MaxPooling2D())
model.add(Conv2D(32, (3, 3), 1, activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(16, (3, 3), 1, activation='relu'))
model.add(MaxPooling2D())
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# TRAIN
logdir = 'logs'
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
hist = model.fit(train_dataset, epochs=20, validation_data=val_dataset, callbacks=[tensorboard_callback])

# PLOT PERFORMANCE
fig = plt.figure()
plt.plot(hist.history['loss'], color='teal', label='loss')
plt.plot(hist.history['val_loss'], color='orange', label='val_loss')
fig.suptitle('Loss', fontsize=20)
plt.legend(loc="upper left")
plt.show()

fig = plt.figure()
plt.plot(hist.history['accuracy'], color='teal', label='accuracy')
plt.plot(hist.history['val_accuracy'], color='orange', label='val_accuracy')
fig.suptitle('Accuracy', fontsize=20)
plt.legend(loc="upper left")
plt.show()

# EVALUATE
# Evaluate the model on the test dataset
eval_metrics = model.evaluate(test_dataset, verbose=0)

# Calculate precision, recall, and accuracy using sklearn.metrics
# Evaluate the model on the test dataset
eval_metrics = model.evaluate(test_dataset, verbose=0)

# Calculate precision, recall, and accuracy using sklearn.metrics
y_true = np.argmax(test_labels, axis=1)  # Convert one-hot encoded labels back to categorical
y_pred = np.argmax(model.predict(test_dataset), axis=1)[:len(y_true)]

precision = precision_score(y_true, y_pred, average='weighted')
recall = recall_score(y_true, y_pred, average='weighted')
accuracy = accuracy_score(y_true, y_pred)

print('Precision:', precision)
print('Recall:', recall)
print('Accuracy:', accuracy)

# SAVING MODEL
model.save(os.path.join('models', 'skinToneClassifier.h5'))