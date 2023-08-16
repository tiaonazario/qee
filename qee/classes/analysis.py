"""
Modulo para analise da qualidade de energia
"""

from typing import Literal

from pandas import DataFrame, read_csv, Series


from qee.classes.voltage import Voltage
from qee.classes.graph import Graph
from qee.enums.consumer_type import ConsumerType
from qee.enums.voltage_level import VoltageLevel
from qee.enums.voltage_type import VoltageType


class VoltageAnalysis:
    """
    Executa a analise de tensão

    Parameters:
        data_frame: data_frame com os dados de tensão
        key: chave do data_frame
        reference: tipo de tensão de referência
    """

    def __init__(
        self, data_frame: DataFrame, key: str, reference: VoltageType
    ) -> None:
        self.data_frame: DataFrame = data_frame
        self.nla: int = 0
        self.nlp: int = 0
        self.nlc: int = 0
        self.key: str = key
        self.reference: VoltageType = reference
        self._classify()

    def _classify(self) -> None:
        """Classifica os números de leituras em adequada, precária ou crítica"""

        voltages: Series[float] = self.data_frame[self.key]
        for value in voltages:
            voltage_instance: Literal[
                VoltageLevel.CRITICAL,
                VoltageLevel.ADEQUATE,
                VoltageLevel.PRECARIOUS,
            ] = Voltage(self.reference).classify(value)
            if voltage_instance == VoltageLevel.ADEQUATE:
                self.nla += 1
            elif voltage_instance == VoltageLevel.PRECARIOUS:
                self.nlp += 1
            else:
                self.nlc += 1

    def drp(self) -> float:
        """Calcula o DRP"""

        return (self.nlp / 1008) * 100

    def drc(self) -> float:
        """Calcula o DRC"""

        return (self.nlc / 1008) * 100

    def compensate(self, consumer: ConsumerType, eusd: float) -> float:
        """
        Calcula a compensação de tensão

        Parameters:
            consumer: tipo de consumidor
            eusd: Encargo de Uso do Sistema de Distribuição (EUSD)
        """

        drp_limit = 3
        drc_limit = 0.5

        const_k1: Literal[3, 0] = 3 if self.drp() > drp_limit else 0

        const_k2 = 0
        if self.drc() <= drc_limit:
            const_k2 = 0
        elif self.drc() > drc_limit and consumer == ConsumerType.BT:
            const_k2 = 7
        elif self.drc() > drc_limit and consumer == ConsumerType.MT:
            const_k2 = 5
        elif self.drc() > drc_limit and consumer == ConsumerType.AT:
            const_k2 = 3

        return (
            ((self.drp() - drp_limit) / (100) * const_k1)
            + ((self.drc() - drc_limit) / (100) * const_k2)
        ) * eusd

    def graph(self, x_key: str) -> Graph:
        """
        Gera gráficos com valores fornecidos

        Parameters:
            x_key: chave do data_frame para os valores do eixo x

        Returns:
            Graph: instância da classe Graph com os dados do gráfico

        Raises:
            ValueError: caso a chave não seja encontrada no data_frame

        Examples:
            >>> analysis = Analysis('data.csv')
            >>> analysis.graph('Tensão')
            Graph(x_values=x_values, y_values=y_values)
        """

        if x_key not in self.data_frame.columns:
            raise ValueError(f"Chave '{x_key}' não encontrada no data_frame")

        # x_values: Series[float] = self.data_frame[x_key]
        # y_values: Series[float] = self.data_frame[self.key]

        graph = Graph(self.data_frame, x_key, self.key)
        return graph


class Analysis:
    """
    Analisa a QEE de acordo com o PRODIST Modulo 8

    Parameters:
        file_path: caminho do arquivo
    """

    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.data_frame: DataFrame = self.load_file()

    def load_file(self) -> DataFrame:
        """Carrega o arquivo em um data_frame com o pandas"""
        file: DataFrame = read_csv(self.file_path, sep=";").head(1008)

        return file

    def voltage(self, key: str, reference: VoltageType) -> VoltageAnalysis:
        """
        Analisa a QEE com relação a tensão em regime permanente

        Parameters:
            key: chave do data_frame
            reference: tipo de tensão de referência

        Returns:
            VoltageAnalysis: instância da classe VoltageAnalysis com os dados da tensão analisada

        Raises:
            ValueError: caso a chave não seja encontrada no data_frame

        Examples:
            >>> analysis = Analysis('data.csv')

            >>> analysis.voltage('Tensão', VoltageType.V220)
            VoltageAnalysis(data_frame=data_frame, key='Tensão', reference=VoltageType.V220)
        """

        if key not in self.data_frame.columns:
            raise ValueError(f"Chave '{key}' não encontrada no data_frame")

        return VoltageAnalysis(self.data_frame, key, reference)
