from tensorflow.keras.preprocessing.image import ImageDataGenerator

class HairGenerator():
    def __init__(self):
        self.hairdatagen = None
        self.hair_flow = None
        
    def datagen(self,
                X,
                y,
                batch_size,
                rotation_range = 30,
                width_shift_range = 0.2,
                height_shift_range = 0.2,
                horizontal_flip = True,
                fill_mode = 'constant',
                cval = 255.,
                brightness_range = [0.6,1.8]
                ):
        self.hairdatagen = ImageDataGenerator(
                            rotation_range = rotation_range,
                            width_shift_range = width_shift_range,
                            height_shift_range = height_shift_range,
                            horizontal_flip = horizontal_flip,
                            fill_mode = fill_mode,
                            cval = cval,
                            brightness_range = brightness_range) 
        self.hairdatagen.fit(X)
     
        self.hair_flow = self.hairdatagen.flow(X, y, batch_size=batch_size)
        
    
