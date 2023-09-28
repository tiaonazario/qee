from typing import Literal

from qee.constants import prodist
from qee.types import VoltageClassifyType, VoltageValueType


class VoltageVariation:
    """Variação de tensão"""

    def __init__(
        self, voltages: list[float], reference: VoltageValueType
    ) -> None:
        self.voltages = voltages
        self.reference: VoltageValueType = reference

        self.__drp: float = 0
        self.__drc: float = 0

    def classify(self, value: float) -> VoltageClassifyType:
        """Classifica a tensão em Critica, Precária ou Adequada"""

        voltage_range = prodist.VOLTAGE_RANGE[self.reference]

        if value < voltage_range['cr-inf'] or value > voltage_range['cr-sup']:
            return 'Crítica'
        if voltage_range['ad-inf'] <= value <= voltage_range['ad-sup']:
            return 'Adequada'

        return 'Precária'

    def reading_number(self) -> list[int]:
        """Calcula o número de leituras adequadas, precárias e críticas"""

        adequate_number = 0
        precarious_number = 0
        critical_number = 0

        for value in self.voltages:
            classification = self.classify(value)

            if classification == 'Adequada':
                adequate_number += 1
            elif classification == 'Precária':
                precarious_number += 1
            else:
                critical_number += 1

        return [adequate_number, precarious_number, critical_number]

    def indicators(self) -> dict[Literal['DRP', 'DRC'], float]:
        """
        Calcula os indicadores Duração Relativa de Transgressão
        para tensão precária e crítica
        """

        numbers = self.reading_number()

        self.__drp = (numbers[1] / 1008) * 100
        self.__drc = (numbers[2] / 1008) * 100

        return {'DRP': self.__drp, 'DRC': self.__drc}
