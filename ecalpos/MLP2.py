#https://www.tensorflow.org/tutorials/keras/basic_regression

from __future__ import absolute_import, division, print_function

import tensorflow as tf
from tensorflow import keras

import numpy as np
from calibratedata import ReadTrainData
readtraindf=ReadTrainData()
train_data = readtraindf[['ch'+str(k) for k in range(9)]].iloc[0:300000]
train_labels = readtraindf['standPosy'].iloc[0:300000]

test_data = readtraindf[['ch'+str(k) for k in range(9)]].iloc[300000:350000]
test_labels = readtraindf['standPosy'].iloc[300000:350000]

mean = train_data.mean(axis=0)
std = train_data.std(axis=0)
train_data = (train_data - mean) / std
test_data = (test_data - mean) / std

def build_model():
    model = keras.Sequential([
    keras.layers.Dense(64, activation=tf.nn.tanh,
                       input_shape=(train_data.shape[1],)),
    keras.layers.Dense(32, activation=tf.nn.tanh),
    keras.layers.Dense(33, activation=tf.nn.tanh),
    keras.layers.Dense(17, activation=tf.nn.tanh),
    keras.layers.Dense(17, activation=tf.nn.tanh),
    keras.layers.Dense(1, activation=tf.nn.relu)
  ])

    optimizer = tf.train.RMSPropOptimizer(0.01)
    # sgd = keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae'])
    return model

model = build_model()
model.summary()


class PrintDot(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs):
        if epoch % 100 == 0:
            pred=model.predict(train_data[0:3000], batch_size=None, verbose=0, steps=None)
            label=np.array(train_labels[0:3000])
            trainstd=np.std(label-pred)
            pred=model.predict(test_data[0:5000], batch_size=None, verbose=0, steps=None)
            label=np.array(test_labels[0:5000])
            teststd=np.std(label-pred)
            print('trainstd:',trainstd,'teststd',teststd,"mean:",np.mean(label-pred))
        # print('.', end='')


EPOCHS = 50000

# Store training stats
history = model.fit(train_data, train_labels, epochs=EPOCHS,batch_size=30000,
                    validation_split=0.2, verbose=0,shuffle=False,
                    callbacks=[PrintDot()])


import matplotlib.pyplot as plt
def plot_history(history):
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('Mean Abs Error [1000$]')
    plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),
             label='Train Loss')
    plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),
             label = 'Val loss')
    plt.legend()
    plt.ylim([0, 0.5])

plot_history(history)

# np.std(label-pred)
