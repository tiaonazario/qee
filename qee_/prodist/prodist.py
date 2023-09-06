from qee.drt import DRT
from qee.indicators_dh import IndicatorsDH
from qee.prodist.voltage_range import VoltageRange


class PRODIST:
    """Classe para trabalhar com o PRODIST"""

    def voltage_range(self) -> VoltageRange:
        """
        Faixa de variação de tensão de leitura fornecida pelo PRODIST
        """
        return VoltageRange()

    def drt_limit(self) -> DRT:
        """
        Limite de DRT para leitura do PRODIST, valores em %
        """
        return DRT(drp=3.0, drc=0.5)

    def dht_limit(self) -> IndicatorsDH:
        """
        Limite de das distorções harmônicas totais para leitura do PRODIST, valores em %
        """
        return IndicatorsDH(10, 2.5, 7.5, 6.5)

    def fd_limit(self) -> float:
        """Limite do fator de desequilíbrio de tensão para leitura do PRODIST, valores em %"""
        return 3.0
