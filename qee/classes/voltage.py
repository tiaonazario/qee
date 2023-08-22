"""
Define a classe para tensão
"""

from qee.classes.prodist import PRODIST
from qee.enums.voltage_level import VoltageLevel
from qee.enums.voltage_value import VoltageValue


class NL:
    """
    Classe para trabalhar com a quantidade de leituras de tensão
    """

    def __init__(self) -> None:
        self.nla: int = 0
        self.nlp: int = 0
        self.nlc: int = 0

    def __str__(self) -> str:
        return f'{{"nla": {self.nla}, "nlp": {self.nlp}, "nlc": {self.nlc}}}'


class DRT:
    """
    Classe para trabalhar com a Duração Relativa da Transgressão, para Tensão Precária e Crítica
    """

    def __init__(self) -> None:
        self.drp: float = 0
        self.drc: float = 0

    def __str__(self) -> str:
        return f'{{"drp": {self.drp:.2f}, "drc": {self.drc:.2f}}}'


class Voltage:
    """
    Classe para trabalhar com uma tensão em volts

    Examples:
        >>> voltage = Voltage()
    """

    def __init__(self) -> None:
        self.__nl = NL()

    def classify(
        self, voltage: float, reference: VoltageValue
    ) -> VoltageLevel:
        """
        Classifica a tensão em Critica, Precária ou Adequada.

        Parameters:
            voltage: Tensão lida para classificação
            reference: Tensão de referência para classificação

        Returns:
            VoltageLevel: Classificação da tensão

        Examples:
            >>> voltage = Voltage(220)

            >>> voltage.classify(250)
            VoltageLevel.CRITICAL

            >>> voltage.classify(220)
            VoltageLevel.ADEQUATE

            >>> voltage.classify(190)
            VoltageLevel.PRECARIOUS
        """

        variation: dict[str, int] = PRODIST().get_voltage_range(reference)

        if voltage < variation['cr-inf'] or voltage > variation['cr-sup']:
            return VoltageLevel.CRITICAL
        if variation['ad-inf'] < voltage < variation['ad-sup']:
            return VoltageLevel.ADEQUATE

        return VoltageLevel.PRECARIOUS

    def reading_number(
        self, voltages: list[float], reference: VoltageValue
    ) -> NL:
        """
        Calcula o número de leituras adequadas, precárias e críticas

        Parameters:
            voltages: Lista com valores de tensão lidas
            reference: Tensão de referência para classificação

        Returns:
            ReadingNumber: NÚmero de leituras adequadas, precárias e críticas

        Raises:
            ValueError: Quantidade de leituras inválida

        Notes:
            Atenção: A quantidade de leituras deve ser igual a 1008

        Examples:
            >>> voltage = Voltage()
            >>> reading_number = voltage.reading_number([220, 250, 190], 220)
            {"nla": 1, "nlp": 1, "nlc": 1}
        """

        if len(voltages) != 1008:
            raise ValueError(
                'Quantidade de leituras inválida, forneça 1008 valores de tensões lidas'
            )

        for voltage in voltages:
            instance_voltage: VoltageLevel = self.classify(voltage, reference)

            if instance_voltage == VoltageLevel.ADEQUATE:
                self.__nl.nla += 1
            elif instance_voltage == VoltageLevel.PRECARIOUS:
                self.__nl.nlp += 1
            else:
                self.__nl.nlc += 1

        return self.__nl

    def relative_duration_transgress(self) -> DRT:
        """
        Calcula a duração relativa da transgressão, para Tensão Precária e Crítica

        Returns:
            DRT: Duração relativa da transgressão, para Tensão Precária e Crítica

        Examples:
            >>> voltage = Voltage()
            >>> voltage.reading_number([220, 250, 190], 220)
            {"nla": 1, "nlp": 1, "nlc": 1}

            >>> voltage = Voltage()
            >>> voltage.reading_number([220, 250, 190], 220)
            >>> voltage.relative_duration_transgress()
            {"drp": 1.00%, "drc": 1.00%}
        """

        drt = DRT()
        drt.drp = (self.__nl.nlp / 1008) * 100
        drt.drc = (self.__nl.nlc / 1008) * 100

        return drt
