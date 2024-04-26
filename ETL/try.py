import pandas as pd 

df1=pd.read_csv('data\Algeria\Weather_1920-1929_ALGERIA.csv',sep=',',encoding='cp1252')
unique_values = df1['TMIN_ATTRIBUTES'].unique()
value_counts = df1['TMIN_ATTRIBUTES'].value_counts()
print(value_counts)