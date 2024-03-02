from datetime import datetime
from typing import Literal

import pandas as pd

from qee.classes import Graphic

VoltageType = Literal['Avg', 'Max', 'Min']
TipoType = Literal['fase', 'linha']
ValoresType = Literal['média', 'máxima', 'mínima']

with open('model_x1.tex', 'r', encoding='utf-8') as file:
    modelo = file.read()

data = pd.read_csv('data/data2.csv', sep=';')


def gera_grafico(amostra: str, voltage: VoltageType, tipo: TipoType):
    """Gera gráfico"""

    options: dict[TipoType, tuple[int, int, int]] = {
        'fase': (1, 2, 3),
        'linha': (12, 23, 31),
    }

    voltages: dict[VoltageType, ValoresType] = {
        'Avg': 'média',
        'Max': 'máxima',
        'Min': 'mínima',
    }

    numbers = options[tipo]
    labels = [f'V{number}_{voltage} [V]' for number in numbers]
    prop = voltages[voltage]
    reference = 220 if tipo == 'fase' else 380

    x_labels: list[str] = data['Time'].to_list()
    x_axis = [
        datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in x_labels
    ]

    content = ''
    for label in labels:
        y_axis: list[float] = data[label].to_list()

        latex = modelo.replace('[TIPO]', tipo)
        latex = latex.replace('[PROP]', prop)

        graphic = Graphic()
        graphic.axes.plot(x_axis, y_axis, label=label)
        graphic.voltage(reference)

        label_ = label.replace(' [V]', '')
        filename = amostra + '_' + label_ + '.pdf'

        save_directory = 'D:/www/github/tcc-engenharia-eletrica/monografia/illustrations/figures'
        graphic.save(f'{save_directory}/{filename}')

        latex = latex.replace('[LABEL]', filename)
        latex = latex.replace('[VALUE]', label_.replace(label_[-4:], ''))

        content += latex + '\n'

    return content


CONTENT = ''

CONTENT += gera_grafico('a2', 'Avg', 'fase')
CONTENT += gera_grafico('a2', 'Max', 'fase')
CONTENT += gera_grafico('a2', 'Min', 'fase')
CONTENT += gera_grafico('a2', 'Avg', 'linha')
CONTENT += gera_grafico('a2', 'Max', 'linha')
CONTENT += gera_grafico('a2', 'Min', 'linha')

with open('grafico.tex', 'w', encoding='utf-8') as file:
    file.write(CONTENT)
