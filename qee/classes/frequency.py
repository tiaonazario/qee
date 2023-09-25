from tabulate import tabulate

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
            self.__classify = "Baixa"
            return self.__classify
        elif self.value > prodist.FREQUENCY_LIMIT[1]:
            self.__classify = "Alta"
            return self.__classify
        else:
            self.__classify = "Adequada"
            return self.__classify

    def print_classify(self):
        """Imprime a classificação da frequência"""

        classify = self.__classify

        print("Classificação da frequência".center(40))
        data = {"Frequência": [self.value], "Classificação": [classify]}
        print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
