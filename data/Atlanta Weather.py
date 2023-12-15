import pandas as pd

df_15_17 = pd.read_excel('Atlanta 2015-01-01 to 2017-08-31.xlsx', sheet_name='Weather Data')
df_17_20 = pd.read_excel('Atlanta 2017-09-01 to 2020-04-30.xlsx', sheet_name='Weather Data')
df_20_21 = pd.read_excel('Atlanta 2020-05-01 to 2021-12-31.xlsx', sheet_name='Weather Data')
df_21_22 = pd.read_excel('Atlanta 2022-01-01 to 2022-12-31.xlsx', sheet_name='Weather Data')
df_22_23 = pd.read_excel('Atlanta 2023-01-01 to 2023-10-31.xlsx', sheet_name='Weather Data')

frames = [df_15_17, df_17_20, df_20_21, df_21_22, df_22_23]

result = pd.concat(frames)

result.to_excel('Atlanta Weather.xlsx')