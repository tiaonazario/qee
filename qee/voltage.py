from .prodist.prodist import PRODIST
from .enums.voltage_value import VoltageValue
from .enums.voltage_type import VoltageType


class Voltage:
    """Classe para trabalhar com valores de tensão"""

    def __init__(self, value: float) -> None:
        self.value = value

    def classify(self, reference: VoltageValue) -> VoltageType:
        """Classifica a tensão em Critica, Precária ou Adequada"""

        prodist = PRODIST()
        variation = prodist.voltage_range().get_one(reference)

        if (
            self.value < variation["cr-inf"]
            or self.value > variation["cr-sup"]
        ):
            return VoltageType.CRITICAL
        if variation["ad-inf"] <= self.value <= variation["ad-sup"]:
            return VoltageType.ADEQUATE

        return VoltageType.PRECARIOUS
