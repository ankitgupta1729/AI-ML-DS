"""
Train an MNIST image recognition model.
"""

import os

import keras
import numpy as np
import tensorflow as tf
from keras.datasets import mnist
from keras.layers import Conv2D, Dense, Dropout, Flatten, Input, MaxPooling2D
from keras.models import Sequential

MODEL_PATH = os.environ.get('MODEL_PATH', 'var/data/mnist.keras')
EPOCHS = int(os.environ.get('EPOCHS', 5))

print(tf.config.list_physical_devices())

# training data -- scaled to 0..1, and given an explicit single (grayscale)
# channel. The serving code in mnist.py must scale incoming images the same way.
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = np.expand_dims(x_train.astype('float32') / 255.0, -1)
x_test = np.expand_dims(x_test.astype('float32') / 255.0, -1)
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

# our convolutional model
input_shape = x_train[0].shape
num_classes = 10
model = Sequential()
model.add(Input(shape=input_shape))
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))
print(model.summary())

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
history = model.fit(x_train, y_train,
                    batch_size=64,
                    epochs=EPOCHS,
                    verbose=1,
                    validation_data=(x_test, y_test))

# save the model in the native keras format
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
model.save(MODEL_PATH)
print('saved', MODEL_PATH)
