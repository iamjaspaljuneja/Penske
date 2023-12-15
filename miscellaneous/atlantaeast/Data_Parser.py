import pandas as pd

data = pd.read_excel('Data_With_Weather_Atlanta_East.xlsx', sheet_name='Sheet1')

data_gas = data.loc[data['GROUP'] == 2]

result_gas = data_gas.drop_duplicates(subset=['DATE OUT'])


data_parcel = data.loc[data['GROUP'] == 3]

result_parcel = data_parcel.drop_duplicates(subset=['DATE OUT'])

result_gas.to_excel('Data_Gas_Atlanta_East_Parsed.xlsx', index=False)

result_parcel.to_excel('Data_Parcel_Atlanta_East_Parsed.xlsx', index=False)