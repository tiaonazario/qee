from tabulate import tabulate

from qee.constants import prodist
from qee.enums import FrequencyClassify


class Frequency:
    """Trabalha com frequência"""

    def __init__(self, value: float) -> None:
        self.value = value
        self.__classify: FrequencyClassify | None = None

    def classify(self) -> FrequencyClassify:
        """Classifica a frequência"""
        if self.value < prodist.FREQUENCY_LIMIT[0]:
            self.__classify = FrequencyClassify.LOW
            return self.__classify
        elif self.value > prodist.FREQUENCY_LIMIT[1]:
            self.__classify = FrequencyClassify.HIGH
            return self.__classify
        else:
            self.__classify = FrequencyClassify.ADEQUATE
            return self.__classify

    def print_classify(self):
        """Imprime a classificação da frequência"""

        classify = None if self.__classify is None else self.__classify.value

        print('Classificação da frequência'.center(40))
        data = {'Frequência': [self.value], 'Classificação': [classify]}
        print(tabulate(data, headers='keys', tablefmt='fancy_grid'))
