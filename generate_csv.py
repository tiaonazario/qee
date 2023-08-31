# pyright: reportUnknownVariableType=none
# pyright: reportUnknownMemberType=none

import pandas as pd

df_h = pd.read_excel('./data/tensao.xls').head(1008)
df_v = pd.read_excel('./data/harmonico.xls').head(1008)
data_frame = pd.merge(df_h, df_v, on='Time')
# print(data_frame)
# data_frame.to_csv("data/data.csv", sep=";", index=False)
# df_h.to_csv("data/data_h.csv", sep=";", index=False)
# df_v.to_csv("data/data_v.csv", sep=";", index=False)
