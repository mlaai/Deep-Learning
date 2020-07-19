import tensorflow as tf 
from os import path, getcwd, chdir

class trainCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get('accuracy') > 0.998):
            print("\nReached {99.8}% accuracy so cancelling training!")
            self.model.stop_training = True

def train_mnist():
    mnist = tf.keras.datasets.mnist
    (x_train, y_train),(x_test, y_test) = mnist.load_data()

    x_train = x_train.reshape(60000, 28, 28, 1)
    x_train  = x_train / 255.0
    x_test = x_test.reshape(10000, 28, 28, 1)
    x_test = x_test / 255.0

    callbacks = trainCallback()

    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D(2, 2),
        tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D(2,2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation=tf.nn.relu),
        tf.keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train, epochs=20, callbacks=[callbacks])

    return history.epoch, history.history['accuracy'][-1]

train_mnist()
