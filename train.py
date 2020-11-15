#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import LSTM, Dense, Activation,Dropout,Embedding
import pandas as pd
import keras.utils
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from sklearn.preprocessing import LabelEncoder
import numpy as np
from keras.datasets import imdb

max_words = 1000
batch_size = 32
epochs = 5

df = pd.read_json('articles_clean.json').astype(str)
articles = len(df['id'].values)
X_raw = df['query'].values
Y_raw = df['id'].values

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(X_raw)
x_train = tokenizer.texts_to_matrix(X_raw)

encoder = LabelEncoder()
encoder.fit(Y_raw)

encoded_Y = encoder.transform(Y_raw)
y_train = keras.utils.to_categorical(encoded_Y, articles)

model = Sequential()
model.add(Dense(512, input_shape=(max_words,)))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(articles))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1)

model.save('articles.h5')
