

# train

import numpy as np
import pandas as pd
from keras.models import *
from keras.layers import *
from keras.utils import np_utils

train_size = 1600
img_cols, img_rows = 50, 90
n_class = 2

data = pd.read_csv('DSCN0003.csv')
data_y = np_utils.to_categorical(data['label'],2)
data_X = np.array(data.iloc[:,:(data.shape[1]-1)])

train_X = data_X[:train_size,:]
train_X = train_X.reshape(train_X.shape[0], img_rows, img_cols, 1)
test_X = data_X[train_size:,:]
test_X = test_X.reshape(test_X.shape[0], img_rows, img_cols, 1)
train_y = data_y[:train_size,:]
test_y = data_y[train_size:,:]

inputs = Input((img_rows, img_cols, 1))
x = inputs

for i in range(3):
    x = Convolution2D(8*2**i, (3,3), activation='relu')(x)
    x = Convolution2D(8*2**i, (3,3), activation='relu')(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2,2))(x)

x = Flatten()(x)
x = Dropout(0.05)(x)
x = Dense(n_class, activation='softmax')(x)

model = Model(inputs=inputs, outputs=x)
model.summary()

model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])
model.fit(train_X, train_y, epochs=5, batch_size=128, validation_data=(test_X,test_y))

model.save('secchi_classification.h5')
