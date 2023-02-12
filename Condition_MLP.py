import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation


file_path = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/"
train_raw = pd.read_pickle(file_path+"daily_motion_train.pickle")
test_raw = pd.read_pickle(file_path+"daily_motion_test.pickle")


def preprocessing(data):
    data = data.loc[data["mental_disorder"].isnull() == False] #only take people with conditiona
    data["melanch"] = data["melanch"].fillna(data["melanch"].dropna().mode())
    data = data.drop(columns=['edu', 'madrs1', 'madrs2', "name"])
    one_hot = pd.get_dummies(data["age"])
    data = data.drop("age", axis = 1)
    data = data.join(one_hot)
    output = data.sample(frac = 1)
    return output
preprocessing(train_raw).to_csv(file_path+"dummy.csv", index=False)

x_train = tf.convert_to_tensor(preprocessing(train_raw).drop(columns=["mental_disorder"]), dtype=tf.float64) 
y_train = tf.convert_to_tensor(preprocessing(train_raw)["mental_disorder"], dtype=tf.float64) 
x_test = tf.convert_to_tensor(preprocessing(test_raw).drop(columns=["mental_disorder"]), dtype=tf.float64) 
y_test = tf.convert_to_tensor(preprocessing(test_raw)["mental_disorder"], dtype=tf.float64) 


model = Sequential()
model.add(keras.Input(shape=x_train.shape))
model.add(Dense(512, activation='relu'))
#model.add(Dense(768, activation='relu'))


model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100, verbose=1,
          validation_data=(x_test, y_test))



