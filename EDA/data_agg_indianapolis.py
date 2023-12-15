import pandas as pd

ld_trans = pd.read_excel('/Users/tammy/Documents/CWRU/xLab/data/data_agg/Specific Districts HH Local Lite Duty Detail 2015 - YTD 2023_10 (1).xlsx',sheet_name='All Data')
util = pd.read_excel('/Users/tammy/Documents/CWRU/xLab/Penske_F23/atlanta_east/Atlanta_East_15_19_Utilization.xlsx', sheet_name='Sheet1')


ld_trans = ld_trans[ld_trans['DISTRICT'] == "0148 - ATLANTA EAST SUWANEE    "]


ld_trans.reset_index(inplace=True,drop=True)

def categorize_location(location):
    if 'PENSKE' in location:
        return 'Penske'
    elif 'HOME' in location:
        return 'Home Depot'
    else:
        return 'Agent'

# Apply the categorization function to the LOCATION column
ld_trans['LOCATION'] = ld_trans['LOCATION'].apply(categorize_location)

#%% creating extra columns 
ld_trans['DURATION'] = (ld_trans['DATE IN'] - ld_trans['DATE OUT']).dt.total_seconds()/(24*60*60)


ld_trans['MILEAGE PRICE'] = ld_trans['RATE MILE'] * ld_trans['MILES USED']
ld_trans['FUEL LOST'] = ld_trans['FUEL_OUT_LEVEL'] - ld_trans['FUEL_IN_LEVEL']
ld_trans['DAMAGED'] = ((ld_trans['DAMAGE_IN'] == 'Y') & (ld_trans['DAMAGE_OUT'] == 'N')).astype(int)

ld_trans.loc[ld_trans['DURATION'] == 0, 'DURATION'] = 1

ld_trans['BOARD PRICE'] = ld_trans['RATE DAY']*ld_trans['DURATION']
ld_trans['EXP PRICE'] = ld_trans['BOARD PRICE'] + ld_trans['MILEAGE PRICE']

cols = ['DATE OUT','TIME OUT','TIME IN','DATE IN','RATE DAY','RATE WEEK','RATE MILE','MILES USED','FUEL LOST','DAMAGED','DURATION','MILEAGE PRICE','BOARD PRICE','EXP PRICE','GROUP','LOCATION']

ld_trans = ld_trans[cols]

del cols

#%% merging the datasets

start_date = ld_trans['DATE OUT'].min()
end_date = ld_trans['DATE IN'].max()

ld_trans['Date'] = ld_trans['DATE OUT']

date_range = pd.date_range(start=start_date, end=end_date)

df_base = pd.DataFrame(date_range, columns=['Date'])

df_utilization_aligned = df_base.merge(util, on='Date', how='left')
df_combined = ld_trans.merge(df_utilization_aligned, on='Date', how='left')

del start_date, end_date, date_range, df_base, df_utilization_aligned


#%%
print("mapping vehicles")
print(df_combined["Date"])
data = df_combined.dropna().drop('Date',axis=1)
mapping = {'LITE DUTY DIESEL': 1,
           'LITE DUTY GAS': 2,
           'PARCEL VAN-LITE DUTY': 3}

data['GROUP'] = data['GROUP'].replace(mapping)

data.reset_index(inplace=True,drop=True)

del mapping, df_combined
        
data.to_excel('Data_Atlanta_East.xlsx',index=False)




