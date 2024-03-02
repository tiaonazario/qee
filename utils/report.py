from typing import Literal

import pandas as pd

from qee.classes import Analysis

VoltageType = Literal['Avg', 'Max', 'Min']
TipoType = Literal['fase', 'linha']
ValoresType = Literal['média', 'máxima', 'mínima']

data = pd.read_csv('data/data1.csv', sep=';')

voltages: dict[VoltageType, ValoresType] = {
    'Avg': 'média',
    'Max': 'máxima',
    'Min': 'mínima',
}

voltage: VoltageType = 'Avg'
tipo: TipoType = 'fase'


def genarete_labels(voltage: VoltageType, tipo: TipoType):
    options: dict[TipoType, tuple[int, int, int]] = {
        'fase': (1, 2, 3),
        'linha': (12, 23, 31),
    }

    numbers = options[tipo]
    labels = [f'V{number}_{voltage} [V]' for number in numbers]
    reference = 220 if tipo == 'fase' else 380

    return labels, reference


analysis = Analysis(data)
vv = analysis.voltage_variation(labels, reference)


data_frames: list[pd.DataFrame] = []
print(vv)
