from qee.constants import prodist
from qee.enums import PowerFactorClassify


class PowerFactor:
    """Fator de potência"""

    def __init__(self, value: float) -> None:
        self.value = value

    def classify(self) -> PowerFactorClassify:
        """Classifica o fator de potência"""

        if self.value < prodist.FP_INDUTIVO:
            return PowerFactorClassify.LOW
        else:
            return PowerFactorClassify.ADEQUATE
