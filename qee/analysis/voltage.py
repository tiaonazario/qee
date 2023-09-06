from qee.constants import prodist
from qee.enums import VoltageValue, VoltageClassify


class Voltage:
    """Define valores de tensão"""

    def __init__(self, value: float) -> None:
        self.value = value

    def classify(self, reference: VoltageValue):
        """Classifica a tensão em Critica, Precária ou Adequada"""

        voltage_range = prodist.VOLTAGE_RANGE[reference.value]
        value = self.value

        if value < voltage_range["cr-inf"] or value > voltage_range["cr-sup"]:
            return VoltageClassify.CRITICAL
        if voltage_range["ad-inf"] <= self.value <= voltage_range["ad-sup"]:
            return VoltageClassify.ADEQUATE

        return VoltageClassify.PRECARIOUS
