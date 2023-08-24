# # pyright: reportUnknownVariableType=none
# # pyright: reportUnknownMemberType=none

# import pandas as pd

# from qee.classes import Harmonic, Voltage
# from qee.enums import VoltageValue
# from qee.functions import harmonics_cols

# VOLTAGE_FILE_NAME = './data/202304110900_202305011720_6_ET-5061C_tensao.csv'
# HARMONIC_FILE_NAME = (
#     './data/202304110900_202305011720_6_ET-5061C_harmonico.csv'
# )

# voltage_file = pd.read_csv(VOLTAGE_FILE_NAME, sep=';')
# harmonic_file = pd.read_csv(HARMONIC_FILE_NAME, sep=';')

# harmonic_df = harmonic_file[harmonics_cols('V1')]
# values: list[float] = harmonic_df.loc[0].to_list()
# harmonic = Harmonic(values[1:], values[0])

# voltages: list[float] = voltage_file['V1_Avg [V]'].head(1008).to_list()

# voltage = Voltage()
# nl = voltage.reading_number(voltages, VoltageValue.V220)
# drt = voltage.relative_duration_transgress()
# print(nl)
# print(drt)
