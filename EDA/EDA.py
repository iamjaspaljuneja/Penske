#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 14:35:29 2023

@author: ellis
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('Data.csv')
#df = df.loc[df['GROUP'] == 3,:]
df['Supply'] = df['SumOfFLEET'] - df['SumOfRENTED']
data = df.groupby('DATE OUT')['Utilization Rate','RATE DAY','RATE MILE','SumOfFLEET','EXP PRICE','SumOfRENTED','Supply'].mean().reset_index()
data['DATE OUT'] = pd.to_datetime(data['DATE OUT'])
#%%

def create_bar(x,y,xl = 'Bins', yl = 'Count'):
    bins = [i for i in range(int(min(x)), int(max(x)+5), 5)]

    prices = np.digitize(x, bins, right=True)

    y = np.array(y)
    # Calculate mean utilization for each bin, handling the possibility of empty bins
    util = [np.mean(y[prices == i]) if np.any(prices == i) else np.nan for i in range(1, len(bins))]

    # Get the middle point for each bin as x-labels
    x_labels = [(bins[i] + bins[i+1]) / 2 for i in range(len(bins)-1)]

    plt.bar(x_labels, util, width=4) # Adjust the width as needed
    plt.xlabel(xl)
    plt.ylabel(yl)
    plt.show()



#%%

#create_bar(data['RATE DAY'],data['Utilization Rate'],'Board Rate ($)','Utilization Rate')
#create_bar(100*data['Utilization Rate'],data['RATE DAY'],'Utilization Rate','Board Rate ($)')
create_bar(data['RATE DAY'],data['Supply'],'Board Rate','Available Trucks')

#create_bar(100*data['RATE MILE'], data['Utilization Rate'], 'Mileage Rate (¢)', 'Utilization Rate')
#create_bar(data['EXP PRICE'],data['Utilization Rate'],'Expected Price ($)','Utilization Rate')
#create_bar(data['SumOfFLEET'],data['Utilization Rate'],'Fleet Size','Utilization Rate')
#create_bar(data['SumOfFLEET'],data['RATE DAY'],'Fleet Size','Board Rate ($)')
#create_bar(data['SumOfFLEET'],data['RATE MILE'],'Fleet Size','Mileage Rate (¢)')
create_bar(data['SumOfFLEET'],data['SumOfRENTED'],'Total Fleet','Total Rented')





#%% Supply - demand cuves
create_bar(data['Supply'], data['RATE DAY'],'Available Trucks','Board Rate')
create_bar(data['Utilization Rate']*100,data['RATE DAY'],'Utilization','Board Rate')
#%%

plt.plot(data['DATE OUT'].dt.dayofyear,data['SumOfRENTED'].rolling(window=7).mean())
plt.plot(data['DATE OUT'].dt.dayofyear,200*data['Utilization Rate'].rolling(window=7).mean())

plt.plot(data['DATE OUT'].dt.dayofyear,data['SumOfFLEET'].rolling(window=7).mean())
plt.show()

#%% correlation


import seaborn as sns

corr = df.corr()

# Plot heatmap of the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=False, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5, linecolor='black')
plt.title('Correlation Heatmap')
plt.show()

#%%
corr = data.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=False, cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5, linecolor='black')
plt.title('Correlation Heatmap')
plt.show()

sns.pairplot(data)
plt.suptitle('Scatter Plot Matrix', y=1.02)
plt.show()

#%%



