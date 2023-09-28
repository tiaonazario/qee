from qee.constants import prodist
from qee.types import PowerFactorClassifyType


class PowerFactor:
    """Fator de potência"""

    def __init__(self, value: float) -> None:
        self.value = value

    def classify(self) -> PowerFactorClassifyType:
        """Classifica o fator de potência"""

        if self.value < prodist.FP_INDUTIVO:
            return 'Crítico'
        else:
            return 'Adequado'
