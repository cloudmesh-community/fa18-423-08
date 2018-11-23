from keras.models import *
from keras.layers import *

img_cols, img_rows = 320,180
n_class = 2

inputs = Input((img_rows,img_cols,3))
x = inputs

for i in range(5):
    x = Convolution2D(8*2**i, (3,3), activation = 'relu')(x)
    x = Convolution2D(8*2**i, (3,3), activation = 'relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2,2))(x)

x = flatten()(x)
x = Dropout(0.15)(x)
x = Dense(n_class, activation = 'softmax')

model = Model(inputs = inputs, outputs = x)
model.summary()
