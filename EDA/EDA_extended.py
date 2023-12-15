#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:56:19 2023

@author: ellis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Data.csv')
#df = df.loc[df['GROUP'] == 3,:]
df['Supply'] = df['SumOfFLEET'] - df['SumOfRENTED']
df['TIME IN'] = pd.to_datetime(df['TIME IN'])
df['TIME OUT'] = pd.to_datetime(df['TIME OUT'])
df['DATE OUT'] = pd.to_datetime(df['DATE OUT'])
df['DATE IN'] = pd.to_datetime(df['DATE IN'])
data = df.groupby('DATE OUT')['Utilization Rate','RATE DAY','RATE MILE','SumOfFLEET','EXP PRICE','SumOfRENTED','Supply'].mean().reset_index()


#%% Departure anr Returns by hour and day


fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# For the hour of the day
# Plotting Departures
sns.distplot(df['TIME OUT'].dt.hour, bins=list(range(25)), kde=False, label="Departures", ax=axes[0])
# Plotting Returns
sns.distplot(df['TIME IN'].dt.hour, bins=list(range(25)), kde=False, label="Returns", ax=axes[0])
axes[0].set_title('Distribution of Truck Departures and Returns by Hour')
axes[0].set_xlabel('Hour')
axes[0].set_ylabel('Count')
axes[0].legend()

# For the day of the week
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Plotting Departures
sns.distplot(df['DATE OUT'].dt.dayofweek, bins=list(range(8)), kde=False, label="Departures", ax=axes[1], hist_kws=dict(edgecolor="k", linewidth=1))
# Plotting Returns
sns.distplot(df['DATE IN'].dt.dayofweek, bins=list(range(8)), kde=False, label="Returns", ax=axes[1], hist_kws=dict(edgecolor="k", linewidth=1))
axes[1].set_title('Distribution of Truck Departures and Returns by Day of Week')
axes[1].set_xlabel('Day of the Week')
axes[1].set_xticks(list(range(7)))
axes[1].set_xticklabels(days_of_week, rotation=45)
axes[1].set_ylabel('Count')
axes[1].legend()

plt.tight_layout()
plt.show()

#%% Sunday depaxw
df2 = df[df['DATE OUT'].dt.dayofweek == 6]
df3 = df[df['DATE IN'].dt.dayofweek == 6]


sns.distplot(df2['TIME OUT'].dt.hour, bins=list(range(25)), kde=False, label="Departures")
sns.distplot(df3['TIME IN'].dt.hour, bins=list(range(25)), kde=False, label="Returns")
plt.legend()


#%% Revenue Trends

# Calculate revenue from board and mileage
df['BOARD REVENUE'] = df['RATE DAY'] * df['DURATION']
df['MILEAGE REVENUE'] = df['RATE MILE'] * df['MILES USED']

# Create subplots with 1 row and 2 columns
fig, ax = plt.subplots(1, 2, figsize=(20, 6),dpi=600)

# Plot for the pie chart
revenues = df[['BOARD REVENUE', 'MILEAGE REVENUE']].sum()
revenues.plot(
    kind='pie',
    ax=ax[0],  # Use the first axis
    autopct=lambda p: '{:.2f}%\n(${:.2f})'.format(p, (p/100)*revenues.sum()),
    colors=[(0,0,1),(0,.5,0)],
)
ax[0].set_title('Revenue by Board and Mileage Rates')
ax[0].set_ylabel('')

# Plot for the cumulative revenue
cumulative_revenue = df.groupby('DATE OUT')[['BOARD REVENUE', 'MILEAGE REVENUE']].sum().cumsum()
cumulative_revenue.plot(kind='line', ax=ax[1])  # Use the second axis
ax[1].set_title('Cumulative Revenue Over Time')
ax[1].set_ylabel('Cumulative Revenue')
ax[1].grid(True)

plt.tight_layout()
plt.show()



#%% Fleet and Utilization by Month


monthly_supply = df.groupby(df['DATE OUT'].dt.month)[['Supply', 'SumOfFLEET', 'SumOfRENTED','Utilization Rate']].mean()


# Plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# Bar plot for Supply, SumOfFLEET, and SumOfRENTED
monthly_supply[['Supply', 'SumOfFLEET', 'SumOfRENTED']].plot(kind='bar', ax=ax1)
ax1.set_xlabel('Month')
ax1.set_ylabel('Supply and Fleet Size')
ax1.set_title('Supply and Utilization Rate as a Function of Month')
ax1.set_xticks(range(12))  # Use range(12) for x-ticks
ax1.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)

# Line plot for Utilization Rate on a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(range(12), monthly_supply['Utilization Rate'], color='black', marker='o')  # Explicitly provide x-values as range(12)
ax2.set_ylabel('Utilization Rate')
ax2.grid(None)

plt.show()


#%%

agents = df[df['LOCATION'] == 'Agent']
penske = df[df['LOCATION'] == 'Penske']
depot = df[df['LOCATION'] == 'Home Depot']

#%%
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Define a list of dataframes and corresponding labels
dataframes = [agents, penske, depot]
labels = ['Agent', 'Penske', 'Home Depot']

for i, (dataframe, label) in enumerate(zip(dataframes, labels)):
    # For the hour of the day
    sns.distplot(dataframe['TIME OUT'].dt.hour, bins=list(range(25)), kde=False, label="Departures", ax=axes[0, i])
    sns.distplot(dataframe['TIME IN'].dt.hour, bins=list(range(25)), kde=False, label="Returns", ax=axes[0, i])
    axes[0, i].set_title(f'{label} Truck Departures and Returns by Hour')
    axes[0, i].set_xlabel('Hour')
    axes[0, i].set_ylabel('Count')
    axes[0, i].legend()

    # For the day of the week
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    sns.distplot(dataframe['DATE OUT'].dt.dayofweek, bins=list(range(8)), kde=False, label="Departures", ax=axes[1, i], hist_kws=dict(edgecolor="k", linewidth=1))
    sns.distplot(dataframe['DATE IN'].dt.dayofweek, bins=list(range(8)), kde=False, label="Returns", ax=axes[1, i], hist_kws=dict(edgecolor="k", linewidth=1))
    axes[1, i].set_title(f'{label} Truck Departures and Returns by Day of Week')
    axes[1, i].set_xlabel('Day of the Week')
    axes[1, i].set_xticks(list(range(7)))
    axes[1, i].set_xticklabels(days_of_week, rotation=45)
    axes[1, i].set_ylabel('Count')
    axes[1, i].legend()

plt.tight_layout()
plt.show()
#%%

for dataframe, label in zip(dataframes, labels):
    # Calculate revenue
    dataframe['BOARD REVENUE'] = dataframe['RATE DAY'] * dataframe['DURATION']
    dataframe['MILEAGE REVENUE'] = dataframe['RATE MILE'] * dataframe['MILES USED']

    # Create subplots with 1 row and 2 columns
    fig, ax = plt.subplots(1, 2, figsize=(20, 6), dpi=600)

    # Pie chart for Revenue by Board and Mileage Rates
    revenues = dataframe[['BOARD REVENUE', 'MILEAGE REVENUE']].sum()
    revenues.plot(
        kind='pie',
        ax=ax[0],
        autopct=lambda p: '{:.2f}%\n(${:.2f})'.format(p, (p/100)*revenues.sum()),
        colors=[(0,0,1),(0,.5,0)],
    )
    ax[0].set_title(f'{label} Revenue by Board and Mileage Rates')
    ax[0].set_ylabel('')

    # Line plot for Cumulative Revenue Over Time
    cumulative_revenue = dataframe.groupby('DATE OUT')[['BOARD REVENUE', 'MILEAGE REVENUE']].sum().cumsum()
    cumulative_revenue.plot(kind='line', ax=ax[1])
    ax[1].set_title(f'{label} Cumulative Revenue Over Time')
    ax[1].set_ylabel('Cumulative Revenue')
    ax[1].grid(True)

    plt.tight_layout()
    plt.show()
    
#%%


