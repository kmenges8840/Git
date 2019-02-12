# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 13:53:10 2019

Linear regression model to predict gearbox minimum dimension (height or width)
based on horsepower

@author: Keith Menges
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

#Import CSV to dataframe
df = pd.read_csv('GearData.csv')

#Create Indepent variable datframe
Ind = df[['HP']]

# Create dependent variable dataframe
Dep = df[['HW']]

# Create training and test sets
X_train, X_test, y_train, y_test = train_test_split(Ind, Dep, test_size =.25,
                                                    random_state=42)

# Create the regressor: reg
#reg = LinearRegression()
#reg = KernelRidge(kernel='polynomial',degree=3)
#reg = KernelRidge(kernel='rbf')
reg = SVR()

# Create the prediction space for plotting
prediction_space = np.linspace(min(Ind.values),max(Ind.values)).reshape(-1,1)

# Fit the regressor to the training data
reg.fit(X_train,y_train)

# Predict on the test data: y_pred
y_pred = reg.predict(X_test)

# Compute and print R^2 and RMSE
print("R^2: {}".format(reg.score(X_test, y_test)))
rmse = np.sqrt(mean_squared_error(y_test,y_pred))
print("Root Mean Squared Error: {}".format(rmse))

# Compute predictions over the prediction space: y_pred
y_pred_plot = reg.predict(prediction_space)

# Plot regression line
_= plt.plot(prediction_space, y_pred_plot, color='black', linewidth=3)
_ = plt.plot(X_test,y_test,linestyle='none',marker='.',color='r')
_ = plt.plot(X_train,y_train,linestyle='none',marker='.',color='b')
_ = plt.xlabel('Horsepower')
_ = plt.ylabel('Minimum Geardrive Housing Dimension')
_ = plt.legend(['Predicted','Test Data','Training Data'])
_ 
plt.show()

# Compute 5-fold cross-validation scores: cv_scores
cv_scores = cross_val_score(reg,Ind,Dep,cv=3)

# Print the 5-fold cross-validation scores
print(cv_scores)
print("Average 5-Fold CV Score: {}".format(np.mean(cv_scores)))