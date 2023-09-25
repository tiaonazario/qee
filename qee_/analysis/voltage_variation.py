from tabulate import tabulate

from qee.analysis.voltage import Voltage
from qee.constants import prodist
from qee.enums import VoltageClassify, VoltageValue


class VoltageVariation:
    """Calcula os indicadores de variação de tensão"""

    def __init__(self, voltages: list[float], reference: VoltageValue) -> None:
        self.voltages = voltages
        self.reference = reference

        self.__drp = 0
        self.__drc = 0

    def reading_number(self) -> list[int]:
        """Calcula o número de leituras adequadas, precárias e críticas"""

        adequate_number = 0
        precarious_number = 0
        critical_number = 0

        for value in self.voltages:
            classification = Voltage(value).classify(self.reference)

            if classification == VoltageClassify.ADEQUATE:
                adequate_number += 1
            elif classification == VoltageClassify.PRECARIOUS:
                precarious_number += 1
            else:
                critical_number += 1

        return [adequate_number, precarious_number, critical_number]

    def indicators(self):
        """Calcula os indicadores Duração Relativa de Transgressão para tensão precária e crítica"""

        numbers = self.reading_number()

        self.__drp = (numbers[1] / 1008) * 100
        self.__drc = (numbers[2] / 1008) * 100

        return [self.__drp, self.__drc]

    def show(self):
        """Imprime os indicadores de variação de tensão"""

        print('Variação de tensão'.center(40))
        data = {
            'Indicador': ['DRP', 'DRC'],
            'Obtido': [
                f'{self.__drp:.2f}%',
                f'{self.__drc:.2f}%',
            ],
            'PRODIST': [
                f'{prodist.DRP_LIMIT:.2f}%',
                f'{prodist.DRC_LIMIT:.2f}%',
            ],
        }
        print(tabulate(data, headers='keys', tablefmt='fancy_grid'))
