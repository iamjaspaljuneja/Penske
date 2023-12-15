#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 14:53:33 2023

@author: ellis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#%% creating data sets
events = pd.read_excel('cleveland_concerts_2022_present.xlsx',sheet_name='CombinedSheet')
weather = pd.read_excel('weather.xlsx',sheet_name='datatable')
ld_trans = pd.read_excel('penske consumer lite duty round trip 2022 to 2023 ytd transactions.xlsx',sheet_name='data')
util = pd.read_excel('Utilization_Cleveland.xlsx', sheet_name='Sheet1')


#subset to cleveland district
ld_trans = ld_trans[ld_trans['DISTRICT'] == '5161 - CLEVELAND               ']


ld_trans.reset_index(inplace=True,drop=True)


#%% creating uhaul pricing of cleveland based on standard rates
def create_uhaul_price(current_date, reservation_date, duration, mileage):
    
    #get days reserved in advanced
    adv = (reservation_date - current_date).total_seconds() / (60*60*24)
    
    board_rate = 19.95 * duration
    mileage_rate = .59 if adv >= 2 else .69
    
    return board_rate + mileage_rate * mileage

#%% creating extra columns 


ld_trans['DURATION'] = (ld_trans['DATE IN'] - ld_trans['DATE OUT']).dt.total_seconds()/(24*60*60)


ld_trans['MILEAGE PRICE'] = ld_trans['RATE MILE'] * ld_trans['MILES USED']
ld_trans['FUEL LOST'] = ld_trans['FUEL_OUT_LEVEL'] - ld_trans['FUEL_IN_LEVEL']
ld_trans['DAMAGED'] = ((ld_trans['DAMAGE_IN'] == 'Y') & (ld_trans['DAMAGE_OUT'] == 'N')).astype(int)

bins = np.arange(0, 11, 1)  # This creates an array [0, 1, 2, ..., 10]

# Plot the histogram
plt.hist(ld_trans.loc[ld_trans['DURATION'] <= 10,:]['DURATION'], bins=bins, edgecolor='k', alpha=0.7, align='left')
plt.title('Histogram of DURATION')
plt.xlabel('Duration')
plt.ylabel('Frequency')
# Set the x-ticks to match the bins
plt.xticks(bins)

plt.show()
ld_trans.loc[ld_trans['DURATION'] == 0, 'DURATION'] = 1

ld_trans['BOARD PRICE'] = ld_trans['RATE DAY']*ld_trans['DURATION']
ld_trans['EXP PRICE'] = ld_trans['BOARD PRICE'] + ld_trans['MILEAGE PRICE']

del bins


#%% creating events a binary column


# Assuming you already have a DataFrame called 'events' with a 'Date' column
events['Date'] = pd.to_datetime(events['Date'].str[:12], format='%b %d, %Y')

# Group events by date and count the number of events on each date
event_counts = events.groupby('Date').size().reset_index(name='No. Events')

# Create a continuous range of dates from min_date to max_date
min_date = events['Date'].min()
max_date = events['Date'].max()
all_dates = pd.date_range(min_date, max_date, freq='D')

# Merge the continuous date range with the event counts
df_continuous = pd.DataFrame({'Date': all_dates})
df_continuous = df_continuous.merge(event_counts, on='Date', how='left')

# Fill NaN values in 'event_count' column with 0 (for dates with no events)
df_continuous['No. Events'] = df_continuous['No. Events'].fillna(0).astype(int)

events = df_continuous

del df_continuous, all_dates, min_date, max_date, event_counts


#%% translating weather data to 4 classes, clear, rain, snow, rain & snow
#since the data has no days where there is just snow, we have
# 0 = clear, 1 = just rain, 2 = snow


conditions = [
    (weather['Pcpn.'].isin(['0', '0.0'])) & (weather['Snow'].isin(['0', '0.0'])),
    (~weather['Pcpn.'].isin(['0', '0.0'])) & (weather['Snow'].isin(['0', '0.0'])),
    (~weather['Snow'].isin(['0', '0.0']))
]


choices = [0, 1, 2]

weather['Category'] = np.select(conditions, choices)

# Extract relevant columns
weather = weather[['Date', 'High', 'Low', 'Category']]

weather['Date'] = pd.to_datetime(weather['Date'])

del choices, conditions

#%% 

cols = ['RES CREATED','DATE OUT','TIME OUT','TIME IN','DATE IN','RATE DAY','RATE WEEK','RATE MILE','MILES USED','FUEL LOST','DAMAGED','VEH_TOTAL','DURATION','MILEAGE PRICE','BOARD PRICE','EXP PRICE','GROUP']


ld_trans = ld_trans[cols]

del cols

#%% merging the datasets

start_date = ld_trans['DATE OUT'].min()
end_date = ld_trans['DATE IN'].max()

ld_trans['Date'] = ld_trans['DATE OUT']

date_range = pd.date_range(start=start_date, end=end_date)

# Create a dataframe with this date range
df_base = pd.DataFrame(date_range, columns=['Date'])

# Left join other dataframes with this base dataframe
df_weather_aligned = df_base.merge(weather, on='Date', how='left')
df_events_aligned = df_base.merge(events, on='Date', how='left')
df_utilization_aligned = df_base.merge(util, on='Date', how='left')

# 3. Merge the Data
df_combined = ld_trans.merge(df_weather_aligned, on='Date', how='left')
df_combined = df_combined.merge(df_events_aligned, on='Date', how='left')
df_combined = df_combined.merge(df_utilization_aligned, on='Date', how='left')

del start_date, end_date, date_range, df_base, df_weather_aligned, df_events_aligned, df_utilization_aligned


#%%

data = df_combined.dropna().drop('Date',axis=1)

mapping = {'LITE DUTY DIESEL': 1,
           'LITE DUTY GAS': 2,
           'PARCEL VAN-LITE DUTY': 3}

data['GROUP'] = data['GROUP'].replace(mapping)

data.reset_index(inplace=True,drop=True)
data['UHAUL PRICE'] = [create_uhaul_price(data.loc[i,'RES CREATED'], data.loc[i,'DATE OUT'], data.loc[i,'DURATION'], data.loc[i,'MILES USED']) for i in range(len(data))]

del mapping, df_combined


#%%

data.to_csv('Data.csv',index=False)




