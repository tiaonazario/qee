"""
Define a classe para tensão
"""

from typing import Literal

from qee.classes.prodist import DRT, NLT, VoltageIndicators, VoltageRange
from qee.enums.consumer_type import ConsumerType
from qee.enums.voltage_type import VoltageType
from qee.enums.voltage_value import VoltageValue


class Voltage:
    """
    Classe para trabalhar com uma tensão em volts

    Examples:
        >>> voltage = Voltage()
    """

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

        if voltage < variation['cr-inf'] or voltage > variation['cr-sup']:
            return VoltageType.CRITICAL
        if variation['ad-inf'] < voltage < variation['ad-sup']:
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
            >>> reading_number = voltage.reading_number([220, 250, 190 ...], 220)
            {"nla": 1, "nlp": 1, "nlc": 1}
        """

        if len(voltages) != 1008:
            raise ValueError(
                'Quantidade de leituras inválida, forneça 1008 valores de tensões lidas'
            )

        nla = 0
        nlp = 0
        nlc = 0
        for voltage in voltages:
            instance_voltage: VoltageType = self.classify(voltage, reference)

            if instance_voltage == VoltageType.ADEQUATE:
                nla += 1
            elif instance_voltage == VoltageType.PRECARIOUS:
                nlp += 1
            else:
                nlc += 1

        nlt = NLT(nla, nlp, nlc)

        return nlt

    def relative_duration_transgress(self, nlp: int, nlc: int) -> DRT:
        """
        Calcula a duração relativa da transgressão, para Tensão Precária e Crítica

        Parameters:
            nlp: Número de leituras precárias
            nlc: Número de leituras críticas

        Returns:
            DRT: Duração relativa da transgressão, para Tensão Precária e Crítica

        Examples:
            >>> voltage = Voltage()
            >>> voltage.relative_duration_transgress(86, 24)
            {drp: 1.00%, drc: 1.00%}
        """

        drp: float = (nlp / 1008) * 100
        drc: float = (nlc / 1008) * 100
        drt = DRT(drp, drc)

        return drt

    def indicators(
        self, voltages: list[float], reference: VoltageValue
    ) -> VoltageIndicators:
        nlt: NLT = self.reading_number(voltages, reference)
        drt: DRT = self.relative_duration_transgress(nlt.nlp, nlt.nlc)
        voltage_indicators: VoltageIndicators = VoltageIndicators(nlt, drt)
        return voltage_indicators

    def compensation(
        self,
        drp: float,
        drc: float,
        eusd: float,
        consumer: ConsumerType = ConsumerType.BT,
    ) -> float:
        """
        Calcula a compensação de tensão

        Parameters:
            drp: Duração relativa da transgressão, para Tensão Precária
            drc: Duração relativa da transgressão, para Tensão Crítica
            eusd: Encargo de Uso do Sistema de Distribuição (EUSD)
            consumer: tipo de consumidor

        Returns:
            float: compensação de tensão

        Notes:
            Atenção: A quantidade de leituras deve ser igual a 1008

        Examples:
            >>> voltage = Voltage()
            >>> compensation: float = voltage.compensation(1, 1, 1)
        """

        drt = DRT()
        drp_limit: float = drt.drp_limit()
        drc_limit: float = drt.drc_limit()

        const_k1: Literal[3, 0] = 3 if drp > drp_limit else 0

        const_k2: int = 0
        if drc <= drc_limit:
            const_k2 = 0
        elif drc > drc_limit and consumer == ConsumerType.BT:
            const_k2 = 7
        elif drc > drc_limit and consumer == ConsumerType.MT:
            const_k2 = 5
        elif drc > drc_limit and consumer == ConsumerType.AT:
            const_k2 = 3

        return (
            ((drp - drp_limit) / (100) * const_k1)
            + ((drc - drc_limit) / (100) * const_k2)
        ) * eusd
