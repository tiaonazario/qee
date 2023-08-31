# pyright: reportUnknownVariableType=none
# pyright: reportUnknownMemberType=none

from pandas import DataFrame, Series

from numpy import percentile

from qee.enums.consumer_type import ConsumerType
from qee.enums.voltage_value import VoltageValue
from qee.enums.voltage_type import VoltageType
from qee.graphic import Graphic
from qee.voltage import Voltage
from qee.nlt import NLT
from qee.drt import DRT
from qee.indicators_dh import IndicatorsDH
from qee.prodist.prodist import PRODIST
from qee.harmonic import Harmonic
from qee.voltage_imbalance import VoltageImbalance


class Analysis:
    """
    Classe para analisar os Indicadores de QEE
    """

    def __init__(self, data: DataFrame) -> None:
        self.data = data

    def graphic_voltage(
        self, x_label: str, y_label: str, reference: VoltageValue
    ) -> Graphic:
        """Gera o gráfico das tensões"""

        x_values: list[float] = self.data[x_label].to_list()
        y_values: list[float] = self.data[y_label].to_list()

        print(f"Gerando gráfico {x_label} por {y_label} ...")

        graphic = Graphic(x_values, y_values)
        graphic.voltage(reference)

        return graphic

    def reading_number(self, label: str, reference: VoltageValue) -> NLT:
        """Calcula o número de leituras adequadas, precárias e críticas"""
        voltages: list[float] = self.data[label].to_list()

        if len(voltages) != 1008:
            raise ValueError(
                "Quantidade de leituras inválida, forneça 1008 valores de tensões"
            )

        nla = 0
        nlp = 0
        nlc = 0

        for value in voltages:
            voltage = Voltage(value)
            classification = voltage.classify(reference)

            if classification == VoltageType.ADEQUATE:
                nla += 1
            elif classification == VoltageType.PRECARIOUS:
                nlp += 1
            else:
                nlc += 1

        return NLT(nla, nlp, nlc)

    def relative_duration_transgress(self, nlp: int, nlc: int):
        """
        Calcula a duração relativa da transgressão, para Tensão Precária e Crítica
        """

        drp: float = (nlp / 1008) * 100
        drc: float = (nlc / 1008) * 100

        return DRT(drp, drc)

    def voltage_compensation(
        self,
        drp: float,
        drc: float,
        eusd: float,
        consumer: ConsumerType = ConsumerType.BT,
    ) -> float:
        """
        Calcula a compensação de tensão
        """

        prodist = PRODIST()
        drt_limit = prodist.drt_limit()
        drp_limit = drt_limit.drp
        drc_limit = drt_limit.drc

        const_k1 = 3 if drp > drp_limit else 0

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

    def harmonic_distortions(self, labels: list[str]) -> IndicatorsDH:
        """
        Calcula o percentil 95 dos indicadores de distorção harmônica
        """

        harmonics = self.data[labels]
        dtt_values: list[float] = []
        dtt_p_values: list[float] = []
        dtt__i_values: list[float] = []
        dtt_3_values: list[float] = []

        for items in harmonics.iterrows():
            serie = items[1]
            values: list[float] = serie.to_list()

            harmonic = Harmonic(values, values[0])
            dtt_values.append(harmonic.dtt())
            dtt_p_values.append(harmonic.dtt_p())
            dtt__i_values.append(harmonic.dtt_i())
            dtt_3_values.append(harmonic.dtt_3())

        dtt_95 = float(percentile(dtt_values, 95))
        dtt_p_95 = float(percentile(dtt_p_values, 95))
        dtt_i_95 = float(percentile(dtt__i_values, 95))
        dtt_3_95 = float(percentile(dtt_3_values, 95))

        return IndicatorsDH(
            dtt_95=dtt_95,
            dtt_p_95=dtt_p_95,
            dtt_i_95=dtt_i_95,
            dtt_3_95=dtt_3_95,
        )

    def voltage_imbalance(
        self, v_ab_label: str, v_bc_label: str, v_ca_label: str
    ) -> float:
        """Calcula o fator de desequilíbrio de tensão de um conjunto de tensões de linha"""

        voltages = self.data[[v_ab_label, v_bc_label, v_ca_label]]

        fds: list[float] = []
        for items in voltages.iterrows():
            series: Series[float] = items[1]
            v_ab = series[v_ab_label]
            v_bc = series[v_bc_label]
            v_ca = series[v_ca_label]

            voltage_imbalance = VoltageImbalance(v_ab, v_bc, v_ca)
            fds.append(voltage_imbalance.factor())
        return float(percentile(fds, 95))
