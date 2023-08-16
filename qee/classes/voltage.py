"""Define a classe para tensão"""

from typing import Literal

from qee.classes.prodist import PRODIST
from qee.enums.voltage_level import VoltageLevel
from qee.enums.voltage_type import VoltageType


class Voltage:
    """
    Classe para trabalhar com uma tensão em volts
    """

    def __init__(self, voltage: VoltageType) -> None:
        self.voltage: VoltageType = voltage

    def classify(
        self, voltage: float
    ) -> Literal[
        VoltageLevel.CRITICAL, VoltageLevel.ADEQUATE, VoltageLevel.PRECARIOUS
    ]:
        """
        Classifica a tensão em Critica, Precária ou Adequada.

        Parameters:
            voltage: Tensão lida para classificação

        Returns:
            VoltageLevel: Classificação da tensão

        Examples:
            >>> self.classify(220)
            VoltageLevel.ADEQUATE

            >>> self.classify(220)
            VoltageLevel.PRECARIOUS

            >>> self.classify(220)
            VoltageLevel.CRITICAL
        """

        variation: dict[str, int] = PRODIST().get_voltage_range(self.voltage)

        if voltage < variation['cr-inf'] or voltage > variation['cr-sup']:
            return VoltageLevel.CRITICAL
        if variation['ad-inf'] < voltage < variation['ad-sup']:
            return VoltageLevel.ADEQUATE

        return VoltageLevel.PRECARIOUS
