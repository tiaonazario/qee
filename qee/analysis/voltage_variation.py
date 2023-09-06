from qee.analysis.voltage import Voltage
from qee.enums import VoltageValue, VoltageClassify


class VoltageVariation:
    """Calcula os indicadores de variação de tensão"""

    def __init__(self, voltages: list[float], reference: VoltageValue) -> None:
        self.voltages = voltages
        self.reference = reference

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

        drp = (numbers[1] / 1008) * 100
        drc = (numbers[2] / 1008) * 100

        return [drp, drc]
