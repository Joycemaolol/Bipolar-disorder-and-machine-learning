import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
file_path = "C:/Users/18jm6/OneDrive - Queen's University/2023 Winter/QMIND 2022-2023/daily_motion.csv"
data = pd.read_csv(file_path)  
data = data[data["mental_disorder"] != "NaN"]
print(data.head())  

one_hot_encoded = pd.get_dummies(data, columns=["age"])

