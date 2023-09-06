import pandas as pd

from qee.analysis import Analysis
from qee.enums import VoltageValue
from qee.utils import harmonic_labels

single_phase = VoltageValue.V220
three_phase = VoltageValue.V380
FILEPATH = "data/csv/data.csv"
MODE = "Avg"
UNITS = " [V]"
V1 = "V1_"
V2 = "V2_"
V3 = "V3_"
V12 = "V12_"
V23 = "V23_"
V31 = "V31_"
AMOUNT_HARMONICS = 20

voltages = [
    [f"{V1}{MODE}{UNITS}", single_phase],
    [f"{V2}{MODE}{UNITS}", single_phase],
    [f"{V3}{MODE}{UNITS}", single_phase],
    [f"{V12}{MODE}{UNITS}", three_phase],
    [f"{V23}{MODE}{UNITS}", three_phase],
    [f"{V31}{MODE}{UNITS}", three_phase],
]

v1_labels = [f"{V1}{MODE}{UNITS}", harmonic_labels(V1, MODE, AMOUNT_HARMONICS)]
v2_labels = [f"{V2}{MODE}{UNITS}", harmonic_labels(V2, MODE, AMOUNT_HARMONICS)]
v3_labels = [f"{V3}{MODE}{UNITS}", harmonic_labels(V3, MODE, AMOUNT_HARMONICS)]

data = pd.read_csv(FILEPATH, sep=";")

analysis = Analysis(data)
# analysis.graphic_voltage(voltages)

analysis.voltage_variation(voltages)
analysis.harmonics([v1_labels, v2_labels, v3_labels])
