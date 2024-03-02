from qee.constants import prodist
from qee.types import FrequencyClassifyType


class Frequency:
    """Frequência"""

    def __init__(self, value: float) -> None:
        self.value = value
        self.__classify: FrequencyClassifyType | None = None

    def classify(self) -> FrequencyClassifyType:
        """Classifica a frequência"""

        if self.value < prodist.FREQUENCY_LIMIT[0]:
            self.__classify = 'Baixa'
        elif self.value > prodist.FREQUENCY_LIMIT[1]:
            self.__classify = 'Alta'
        else:
            self.__classify = 'Adequada'

        return self.__classify
