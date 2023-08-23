"""
Define a classe para tensão
"""

from typing import Literal

from qee.classes.prodist import DRT, NLT, VoltageRange
from qee.enums.consumer_type import ConsumerType
from qee.enums.voltage_type import VoltageType
from qee.enums.voltage_value import VoltageValue


class Voltage:
    """
    Classe para trabalhar com uma tensão em volts

    Examples:
        >>> voltage = Voltage()
    """

    def __init__(self) -> None:
        self.__nlt = NLT()
        self.__drt = DRT()

    def classify(self, voltage: float, reference: VoltageValue) -> VoltageType:
        """
        Classifica a tensão em Critica, Precária ou Adequada.

        Parameters:
            voltage: Tensão lida para classificação
            reference: Tensão de referência para classificação

        Returns:
            VoltageType: Classificação da tensão

        Examples:
            >>> voltage = Voltage(220)

            >>> voltage.classify(250)
            VoltageType.CRITICAL

            >>> voltage.classify(220)
            VoltageType.ADEQUATE

            >>> voltage.classify(190)
            VoltageType.PRECARIOUS
        """

        variation: dict[str, int] = VoltageRange().get_one(reference)

        if voltage < variation["cr-inf"] or voltage > variation["cr-sup"]:
            return VoltageType.CRITICAL
        if variation["ad-inf"] < voltage < variation["ad-sup"]:
            return VoltageType.ADEQUATE

        return VoltageType.PRECARIOUS

    def reading_number(
        self, voltages: list[float], reference: VoltageValue
    ) -> NLT:
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
                "Quantidade de leituras inválida, forneça 1008 valores de tensões lidas"
            )

        for voltage in voltages:
            instance_voltage: VoltageType = self.classify(voltage, reference)

            if instance_voltage == VoltageType.ADEQUATE:
                self.__nlt.nla += 1
            elif instance_voltage == VoltageType.PRECARIOUS:
                self.__nlt.nlp += 1
            else:
                self.__nlt.nlc += 1

        return self.__nlt

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

        self.__drt.drp = (self.__nlt.nlp / 1008) * 100
        self.__drt.drc = (self.__nlt.nlc / 1008) * 100

        return self.__drt

    def compensation(self, consumer: ConsumerType, eusd: float):
        """
        Calcula a compensação de tensão

        Parameters:
            consumer: tipo de consumidor
            eusd: Encargo de Uso do Sistema de Distribuição (EUSD)
        """

        drp_limit: float = self.__drt.drp_limit()
        drc_limit: float = self.__drt.drc_limit()

        const_k1: Literal[3, 0] = 3 if self.__drt.drp > drp_limit else 0

        const_k2: int = 0
        if self.__drt.drc <= drc_limit:
            const_k2 = 0
        elif self.__drt.drc > drc_limit and consumer == ConsumerType.BT:
            const_k2 = 7
        elif self.__drt.drc > drc_limit and consumer == ConsumerType.MT:
            const_k2 = 5
        elif self.__drt.drc > drc_limit and consumer == ConsumerType.AT:
            const_k2 = 3

        return (
            ((self.__drt.drp - drp_limit) / (100) * const_k1)
            + ((self.__drt.drc - drc_limit) / (100) * const_k2)
        ) * eusd
