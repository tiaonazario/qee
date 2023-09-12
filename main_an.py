from typing import List, Tuple

import pandas as pd

from qee.analysis import Analysis
from qee.enums import VoltageValue
from qee.utils import harmonic_labels

single_phase_voltage: VoltageValue = VoltageValue.V220
three_phase_voltage: VoltageValue = VoltageValue.V380
FILEPATH = 'data/csv/data.csv'
MODE = 'Avg'
# MODE = "Min"
# MODE = "Max"
V1: str = f'V1_{MODE} [V]'
V2: str = f'V2_{MODE} [V]'
V3: str = f'V3_{MODE} [V]'
V12: str = f'V12_{MODE} [V]'
V23: str = f'V23_{MODE} [V]'
V31: str = f'V31_{MODE} [V]'
AMOUNT_HARMONICS = 20
FREQUENCY = f'freq_{MODE} [Hz]'

single_phase_voltages: List[Tuple[str, VoltageValue]] = [
    (V1, single_phase_voltage),
    (V2, single_phase_voltage),
    (V3, single_phase_voltage),
]

three_phase_voltages: List[Tuple[str, VoltageValue]] = [
    (V12, three_phase_voltage),
    (V23, three_phase_voltage),
    (V31, three_phase_voltage),
]

# har01V1_Avg [V]
v1_labels = (V1, harmonic_labels(AMOUNT_HARMONICS, 'har', V1))
v2_labels = (V2, harmonic_labels(AMOUNT_HARMONICS, 'har', V2))
v3_labels = (V3, harmonic_labels(AMOUNT_HARMONICS, 'har', V3))

data = pd.read_csv(FILEPATH, sep=';')

analysis = Analysis(data)
# analysis.graphic_voltage(single_phase_voltages)
# analysis.graphic_voltage(three_phase_voltages)
analysis.voltage_variation(single_phase_voltages, pdf_table=True)
analysis.voltage_variation(three_phase_voltages, pdf_table=True)
analysis.harmonics([v1_labels, v2_labels, v3_labels], pdf_table=True)
analysis.voltage_imbalance([V12, V23, V31], pdf_table=True)
analysis.frequency_variation(FREQUENCY, pdf_table=True)
analysis.build_table(f'build/relatorio_{MODE}.pdf')
