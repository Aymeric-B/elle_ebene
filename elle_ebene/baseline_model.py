"""
Creation of a baseline model and record the weights
"""

from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras.callbacks import EarlyStopping

def initialize_model_base():
   
    model  = models.Sequential()
    
    ### First convolution & max-pooling
    model.add(layers.Conv2D(64, kernel_size=(4, 4), activation='relu', input_shape=(500, 500, 3), padding = "same"))
    model.add(layers.MaxPool2D(pool_size = (4,4)))
    model.add(layers.Dropout(rate=0.2))
    
    ### Second convolution
    model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='relu', padding = "same"))
    model.add(layers.MaxPool2D(pool_size = (4,4)))    
    model.add(layers.Dropout(rate=0.2))
    
    ### Third convolution
    model.add(layers.Conv2D(128, kernel_size=(3, 3), activation='relu', padding = "same"))
    model.add(layers.MaxPool2D(pool_size = (4,4)))    
    model.add(layers.Dropout(rate=0.4))
    
    ### Third convolution
    model.add(layers.Conv2D(128, kernel_size=(3, 3), activation='relu', padding = "same"))
    model.add(layers.MaxPool2D(pool_size = (2,2)))    
    model.add(layers.Dropout(rate=0.4))

    ### Flattening
    model.add(layers.Flatten())
    
    ### One fully connected
    model.add(layers.Dense(128, activation='relu')) 
    model.add(layers.Dropout(rate=0.5))

    ### Last layer
    model.add(layers.Dense(2, activation='sigmoid')) 

    model.compile(loss='binary_crossentropy',
            optimizer="adam",
            metrics=['accuracy'])
    
    return model

def train(model):
    es = EarlyStopping(patience=15, restore_best_weights=True)
    model.fit(X_train, y_train, validation_split = 0.2,
          epochs=200, batch_size=8, verbose=1, callbacks = [es])
    return model
