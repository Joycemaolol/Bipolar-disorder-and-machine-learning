import numpy as np; 
import pandas as pd;
import os; 
import matplotlib.pyplot as plt; 

## - Import the dataset properly

Mydata = pd.read_csv('/Users/julienchanel/Documents/GitHub/data/scores.csv')
Mydata

## - show dataset, create new columns with two existing variables\

Mydata.info()
Mydata['Average madrs'] = ((Mydata.madrs2 + Mydata.madrs1)/2)
Mydata

## - Normalize the data [xnormalized = (x - xminimum) / range of x]

## - plot the activity dataset (Q. How to import activity for all conditions - as their in seperate files. Does this mean we'll have to do our analysis from condition to condition)

Activity1 = pd.read_csv('/Users/julienchanel/Documents/GitHub/data/condition/condition_1.csv')
Activity1

Activity1_plot = plt.rcParams['figure.figsize']
plt.rcParams['figure.figsize'] = (14,4)
Activity1.plot(x='timestamp', y=['activity'], kind='line', xlabel='Time')
plt.title('Condition 1, Motor Activity')
plt.grid()
plt.show()
plt.rcParams['figure.figsize'] = Activity1_plot

## - find the length of “0” motion(a range, maybe 0-5) for each patient each day, for unipolar, bipolar, and healthy controls. For each patient, plot a graph: x asis: day, y axis: amount of time with no movement

## - find the “maximum” motion for each patient each day, for unipolar, bipolar, and healthy controls. For each patient, plot a graph: x asis: day, y axis: amount of time with no movement

## - find the “Mean (Average)” motion for each patient each day, for unipolar, bipolar, and healthy controls. For each patient, plot a graph: x asis: day, y axis: amount of time with no movement

Ac1Sum = sum(Activity1.activity)
Activity1['AverageMotion'] = (Ac1Sum/Activity1.count())

Activity1
AverageMotion_plot = plt.rcParams['figure.figsize']
AverageMotion_plot(x='AverageMotion')

## - find the “standard deviation” motion for each patient each day, for unipolar, bipolar, and healthy controls. For each patient, plot a graph: x asis: day, y axis: amount of time with no movement


## - learn how to(it’s ok if you don’t know how to code this at this point) encode data: change categorical data into numerical data





