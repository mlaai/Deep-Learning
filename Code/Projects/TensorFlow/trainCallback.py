import tensorflow as tf 

class trainCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, percent, logs={}):
        if(logs.get('acc') > percent/100):
            print("\nReached {percent} % accuracy so cancelling training!")
            self.model.stop_training = True