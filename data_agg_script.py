# This script combines transaction data with utilization data.
import pandas as pd

# Load data from an Excel file (replace 'your_file.xlsx' with the actual file path)

# This file contains the utilization of each type of truck on a given date.
# [REGION, REGION #, AREA, AREA #, DISTRICT, DIST #, Category, Veh Type, SumOfRENTED, SumOfFLEET, YEAR/MONTH, MONTH, YEAR, REC_DATE]
df = pd.read_excel('/Users/tammy/Documents/CWRU/xLab/data/data_agg/Specific Districts Utilization by Day 2015 - YTD 2023_10 copy.xlsx', sheet_name="All Data")

# This file contains the transaction data.

# [REGION, AREA, DISTRICT, LOCATION, CUSTOMER_KEY, CONTRACT STATUS, RENTAL SOURCE, RENTAL_TYPE, SOURCE_OPTION_NAME, QUOTE CREATED, RES CREATED, CONTRACT CREATED, TRANS #, DATE OUT, TIME OUT, DATE IN, TIME IN, CONTRACT CLOSED, UNIT NUMBER, Category, GROUP, RATE DAY, RATE WEEK, RATE MILE, MILES OUT, MILES IN, MILES USED, FUEL_OUT_LEVEL, FUEL_IN_LEVEL, DAMAGE_OUT, DAMAGE_IN]
ld_trans = pd.read_excel('/Users/tammy/Documents/CWRU/xLab/data/data_agg/Specific Districts HH Local Lite Duty Detail 2015 - YTD 2023_10 (1).xlsx',sheet_name='All Data')

# Fields used to filter the data documents by a specific city
district_id = "0148"
city = "Atlanta_East"
district =  "0148 - ATLANTA EAST SUWANEE    "

# Convert the 'Date' column to a datetime type to ensure proper date handling.
df['Date'] = pd.to_datetime(df['REC_DATE'])

# Filtering for the specific district
df = df[df['DIST #'] == int(district_id)]
df_gas = df[df['Veh Type'] == 'LITE DUTY GAS']
df_parcel = df[df['Veh Type'] == 'PARCEL VAN-LITE DUTY']
df_diesel = df[df['Veh Type'] == 'LITE DUTY DIESEL']
df = df[df['Category'] == 'Light Duty']

# Group the data by 'Date' and sum the 'Value' for each group
summed_rented_all = df.groupby('Date')['SumOfRENTED'].sum().reset_index()
summed_total_all = df.groupby('Date')['SumOfFLEET'].sum().reset_index()

summed_rented_gas = df_gas.groupby('Date')['SumOfRENTED'].sum().reset_index()
summed_total_gas = df_gas.groupby('Date')['SumOfFLEET'].sum().reset_index()

summed_rented_parcel = df_parcel.groupby('Date')['SumOfRENTED'].sum().reset_index()
summed_total_parcel = df_parcel.groupby('Date')['SumOfFLEET'].sum().reset_index()

summed_rented_diesel = df_diesel.groupby('Date')['SumOfRENTED'].sum().reset_index()
summed_total_diesel = df_diesel.groupby('Date')['SumOfFLEET'].sum().reset_index()

summed_rented_all.set_index('Date', inplace=True)
summed_total_all.set_index('Date', inplace=True)

summed_rented_gas.set_index('Date', inplace=True)
summed_total_gas.set_index('Date', inplace=True)

summed_rented_parcel.set_index('Date', inplace=True)
summed_total_parcel.set_index('Date', inplace=True)

summed_rented_diesel.set_index('Date', inplace=True)
summed_total_diesel.set_index('Date', inplace=True)

# Ensure both data frames are sorted by the date
summed_rented_all = summed_rented_all.sort_index()
summed_total_all = summed_total_all.sort_index()

summed_rented_gas = summed_rented_gas.sort_index()
summed_total_gas = summed_total_gas.sort_index()

summed_rented_parcel = summed_rented_parcel.sort_index()
summed_total_parcel = summed_total_parcel.sort_index()

summed_rented_diesel = summed_rented_diesel.sort_index()
summed_total_diesel = summed_total_diesel.sort_index()

# Merge into one dataframe
merged_df_all = pd.merge(summed_rented_all, summed_total_all, on='Date', how='inner')
merged_df_gas = pd.merge(summed_rented_gas, summed_total_gas, on='Date', how='inner')
merged_df_parcel = pd.merge(summed_rented_parcel, summed_total_parcel, on='Date',how='inner')
merged_df_diesel = pd.merge(summed_rented_diesel, summed_total_diesel, on='Date',how='inner')

# Perform element-wise division
merged_df_all['Utilization Rate'] = merged_df_all['SumOfRENTED'] / merged_df_all['SumOfFLEET']
merged_df_gas['Utilization Rate'] = merged_df_gas['SumOfRENTED'] / merged_df_gas['SumOfFLEET']
merged_df_parcel['Utilization Rate'] = merged_df_parcel['SumOfRENTED'] / merged_df_parcel['SumOfFLEET']
merged_df_diesel['Utilization Rate'] = merged_df_diesel['SumOfRENTED'] / merged_df_diesel['SumOfFLEET']

merged_df_all.rename(columns={'Utilization Rate': 'Utilization Rate All', 'SumOfRENTED': 'SumOfRENTED All', 'SumOfFLEET': 'SumOfFLEET All'}, inplace=True)
merged_df_gas.rename(columns={'Utilization Rate': 'Utilization Rate Gas', 'SumOfRENTED': 'SumOfRENTED Gas', 'SumOfFLEET': 'SumOfFLEET Gas'}, inplace=True)
merged_df_parcel.rename(columns={'Utilization Rate': 'Utilization Rate Parcel', 'SumOfRENTED': 'SumOfRENTED Parcel', 'SumOfFLEET': 'SumOfFLEET Parcel'}, inplace=True)
merged_df_diesel.rename(columns={'Utilization Rate': 'Utilization Rate Diesel', 'SumOfRENTED': 'SumOfRENTED Diesel', 'SumOfFLEET': 'SumOfFLEET Diesel'}, inplace=True)

# Create util dataframe which has all the utilization rates for Gas, Disel, Parcel, and All
util = pd.merge(merged_df_diesel, merged_df_gas, on='Date',how='outer')
util['SumOfRENTED Diesel'].fillna(0, inplace=True)
util['SumOfFLEET Diesel'].fillna(0, inplace=True)
util['Utilization Rate Diesel'].fillna(0, inplace=True)
util = pd.merge(util, merged_df_parcel, on='Date',how='outer')
util = pd.merge(util, merged_df_all,on='Date',how='outer')

# Filter the second document by district
ld_trans = ld_trans[ld_trans['DISTRICT'] == district]

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

# Creating columns DURATION, MILEAGE PRICE, FUEL LOST, DAMAGED, BOARD PRICE, EXP PRICE
ld_trans['DURATION'] = (ld_trans['DATE IN'] - ld_trans['DATE OUT']).dt.total_seconds()/(24*60*60)
ld_trans['MILEAGE PRICE'] = ld_trans['RATE MILE'] * ld_trans['MILES USED']
ld_trans['FUEL LOST'] = ld_trans['FUEL_OUT_LEVEL'] - ld_trans['FUEL_IN_LEVEL']
ld_trans['DAMAGED'] = ((ld_trans['DAMAGE_IN'] == 'Y') & (ld_trans['DAMAGE_OUT'] == 'N')).astype(int)
ld_trans.loc[ld_trans['DURATION'] == 0, 'DURATION'] = 1
ld_trans['BOARD PRICE'] = ld_trans['RATE DAY']*ld_trans['DURATION']
ld_trans['EXP PRICE'] = ld_trans['BOARD PRICE'] + ld_trans['MILEAGE PRICE']

# Columns within the file we want to keep
cols = ['DATE OUT','TIME OUT','TIME IN','DATE IN','RATE DAY','RATE WEEK','RATE MILE','MILES USED','FUEL LOST','DAMAGED','DURATION','MILEAGE PRICE','BOARD PRICE','EXP PRICE','GROUP','LOCATION']
ld_trans = ld_trans[cols]

# Determine the time range we are processing
start_date = ld_trans['DATE OUT'].min()
end_date = ld_trans['DATE IN'].max()

# Rename column for consistency
ld_trans['Date'] = ld_trans['DATE OUT']

# Merge the utilization and transaction data by date
date_range = pd.date_range(start=start_date, end=end_date)
df_base = pd.DataFrame(date_range, columns=['Date'])

df_utilization_aligned = df_base.merge(util, on='Date', how='left')
df_combined = ld_trans.merge(df_utilization_aligned, on='Date', how='left')

del start_date, end_date, date_range, df_base, df_utilization_aligned

# Drops any rows that do not have all the fields filled out
data = df_combined.dropna().drop('Date',axis=1)

# Maps the vehicle type to a value
mapping = {'LITE DUTY DIESEL': 1,
           'LITE DUTY GAS': 2,
           'PARCEL VAN-LITE DUTY': 3}

data['GROUP'] = data['GROUP'].replace(mapping)

data.reset_index(inplace=True,drop=True)

# Export the data to an excel file.
data.to_excel('Data_{}.xlsx'.format(city),index=False)
