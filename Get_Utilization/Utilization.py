import pandas as pd

# Load data from an Excel file (replace 'your_file.xlsx' with the actual file path)
df = pd.read_excel('/Users/tammy/Documents/CWRU/xLab/data/data_agg/Specific Districts Utilization by Day 2015 - YTD 2023_10 copy.xlsx', sheet_name="All Data")

# Convert the 'Date' column to a datetime type to ensure proper date handling
df['Date'] = pd.to_datetime(df['REC_DATE'])

df = df[df['DIST #'] == int("0148")]
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

# Print the resulting DataFrame
# print(summed_rented_gas)
# print(summed_total_gas)
#
# print(summed_rented_parcel)
# print(summed_total_parcel)
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

# Print the resulting data frame
# print(merged_df_gas)
# print(merged_df_parcel)

#merged_df_util = pd.merge(merged_df_all, pd.merge(merged_df_diesel, pd.merge(merged_df_gas, merged_df_parcel, on='Date', how='inner'), on='Date',how='inner'), on='Date',how='inner')

merged_df_util = pd.merge(merged_df_diesel, merged_df_gas, on='Date',how='outer')
merged_df_util['SumOfRENTED Diesel'].fillna(0, inplace=True)
merged_df_util['SumOfFLEET Diesel'].fillna(0, inplace=True)
merged_df_util['Utilization Rate Diesel'].fillna(0, inplace=True)
merged_df_util = pd.merge(merged_df_util, merged_df_parcel, on='Date',how='outer')
merged_df_util = pd.merge(merged_df_util, merged_df_all,on='Date',how='outer')

merged_df_util.to_excel('LaMirada_15_19_Utilization.xlsx', index=True)
