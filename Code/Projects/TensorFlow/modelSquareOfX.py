#import libraries
import tensorflow as tf 
import numpy as np
from tensorflow import keras

#define neural network
model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])

#compile neural network
model.compile(optimizer='sgd', loss='mean_squared_error')

#get input data
xs = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
ys = np.array([1.0, 4.0, 9.0, 16.0, 25.0])

#training neural network
model.fit(xs, ys, epochs=500)

#output result
print(model.predict([6]))
