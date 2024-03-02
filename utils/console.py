import pandas as pd

tensao = (
    pd.read_excel('data/tensao.xls').drop(columns=['Unnamed: 0']).head(1008)
)
har = (
    pd.read_excel('data/harmonicos.xls')
    .drop(columns=['Unnamed: 0'])
    .head(1008)
)
freq = (
    pd.read_excel('data/frequencia.xls')
    .drop(columns=['Unnamed: 0'])
    .head(1008)
)
pst = pd.read_excel('data/pst.xls').drop(columns=['Unnamed: 0']).head(1008)

data1 = pd.merge(tensao, har, on='Time')
data2 = pd.merge(data1, freq, on='Time')
data = pd.merge(data2, pst, on='Time')


# print(data)
data.to_csv('data/data2.csv', sep=';')
