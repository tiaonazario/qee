import pandas as pd

data = pd.read_csv('data/csv/data.csv', sep=';')
new_data = data[['V1_Avg [V]', 'V2_Avg [V]', 'V3_Avg [V]']]
series = new_data.values.tolist()

print(series)
