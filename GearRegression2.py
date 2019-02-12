# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import numpy as np
from sklearn import model_selection as msk
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

#Import CSV to dataframe
df = pd.read_csv('GearData.csv')
df = df.sort_values(by=['HP'],kind='mergesort')
df = df.reset_index(drop=True)
df = df.loc[df.loc[:,'HP']<5000, :]

#Create Indepent variable datframe
X = df[['HP']].values

# Create dependent variable dataframe
y = df[['HW']].values

# #############################################################################
# Fit regression model
parameters = { 'kernel':['poly'],
               'degree': [1,2,3]}
         #      'alpha' : [0.9,1.0,1.1]}

krr = KernelRidge()

clf = msk.GridSearchCV(krr, parameters,cv=5) 

clf.fit(X,y)
y_predict = clf.best_estimator_.predict(X)
results = clf.cv_results_
 #############################################################################
# Look at the results
lw = 2
plt.scatter(X, y, color='darkorange', label='data')
plt.plot(X, y_predict, color='navy', lw=lw, label='poly')
plt.xlabel('data')
plt.ylabel('target')
plt.title('Kernel Ridge Regression')
plt.legend()
plt.show()

print(clf.best_params_, clf.best_score_)

## Compute 5-fold cross-validation scores: cv_scores
#cv_scores = msk.cross_val_score(svr_rbf,X,y,cv=5)
#
## Print the 5-fold cross-validation scores
#print(cv_scores)
#print("Average 5-Fold CV Score: {}".format(np.mean(cv_scores)))