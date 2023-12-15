#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:15:07 2023

@author: ellis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('Penske_F23/EDA/Data.csv')


#%%
cols = ['DATE OUT','RATE DAY','RATE MILE','High','Low','Category','No. Events','UHAUL PRICE','Utilization Rate']

df = data[cols]


daily_data = df.groupby('DATE OUT').agg(
    mean_rate_day=('RATE DAY', 'mean'),
    max_rate_day=('RATE DAY', 'max'),
    min_rate_day=('RATE DAY', 'min'),
    variance_rate_day=('RATE DAY', 'var'),
    
    mean_rate_mile=('RATE MILE', 'mean'),
    max_rate_mile=('RATE MILE', 'max'),
    min_rate_mile=('RATE MILE', 'min'),
    variance_rate_mile=('RATE MILE', 'var'),
    
    mean_uhaul = ('UHAUL PRICE','mean'),
    max_uhaul=('UHAUL PRICE', 'max'),
    min_uhaul=('UHAUL PRICE', 'min'),
    var_uhaul=('UHAUL PRICE', 'var'),
    
    events = ('No. Events','max'),
    weather = ('Category','max'),
    
    util=('Utilization Rate','mean')
).reset_index()
#%%
daily_data['DATE OUT'] = pd.to_datetime(daily_data['DATE OUT'])
daily_data['DOM'] = daily_data['DATE OUT'].dt.day
daily_data['DOW'] = daily_data['DATE OUT'].dt.dayofweek

daily_data['variance_rate_day'].fillna(0, inplace=True)
daily_data['variance_rate_mile'].fillna(0, inplace=True)
daily_data['var_uhaul'].fillna(0,inplace=True)


#%%
plt.plot(daily_data['util'],color='blue')
plt.plot(daily_data['util'].rolling(window=7).mean(),color='red')


#%% train and test sets

split = int(.7*len(daily_data))

X_train = daily_data.loc[:split,:].drop(['DATE OUT','util'],axis=1)
y_train = daily_data.loc[:split,'util']

X_test = daily_data.loc[split:,:].drop(['DATE OUT','util'],axis=1)
y_test = daily_data.loc[split:,'util']

#%% Linear Regression

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Initialize the Linear Regression model
lr = LinearRegression()

# Train the model
lr.fit(X_train, y_train)

# Predict on the test set
y_pred_lr = lr.predict(X_test)

# Calculate the mean squared error for the Linear Regression model
mse_lr = mean_squared_error(y_test, y_pred_lr)
print(f"Linear Regression MSE: {mse_lr}")

# Sorting the coefficients in descending order
sorted_coeffs = sorted(zip(X_train.columns, lr.coef_), key=lambda x: x[1], reverse=True)

# Print the intercept
print("Intercept:", lr.intercept_)

# Print the sorted coefficients for each feature
for feature, coef in sorted_coeffs:
    print(f"{feature}: {coef}")

print('________________________________________________')

#%%
from sklearn.tree import DecisionTreeRegressor

# Initialize the Decision Tree model
dt = DecisionTreeRegressor(max_depth=4)

# Train the model
dt.fit(X_train, y_train)

# Predict on the test set
y_pred_dt = dt.predict(X_test)

# Calculate the mean squared error for the Decision Tree model
mse_dt = mean_squared_error(y_test, y_pred_dt)
print(f"Decision Tree MSE: {mse_dt}")

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# Assuming you have already trained a decision tree model named "dt"
plt.figure(figsize=(30, 10),dpi=500)  # Set the figure size
plot_tree(dt, filled=True, feature_names=X_train.columns, rounded=True, fontsize=10)
plt.show()

# Sorting the feature importances in descending order
sorted_importances = sorted(zip(X_train.columns, dt.feature_importances_), key=lambda x: x[1], reverse=True)

# Print the sorted feature importances
for feature, importance in sorted_importances:
    print(f"{feature}: {importance}")


#%%
import matplotlib.pyplot as plt

# Linear Regression Predictions vs Actual
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.scatter(y_test, y_pred_lr, color='red', alpha=0.5, label='Predictions')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='blue', label='y=x line')
plt.title('Linear Regression: Predictions vs Actual')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.legend()
plt.axis('square')

# Decision Tree Predictions vs Actual
plt.subplot(1, 2, 2)
plt.scatter(y_test, y_pred_dt, color='green', alpha=0.5, label='Predictions')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='blue', label='y=x line')
plt.title('Decision Tree: Predictions vs Actual')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.legend()
plt.axis('square')

plt.tight_layout()
plt.show()
