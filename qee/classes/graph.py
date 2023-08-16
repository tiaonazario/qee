"""Classe para geração de gráficos"""

from pandas import Series, DataFrame
from matplotlib.pyplot import subplots, savefig, Axes, show as plt_show
from matplotlib.figure import Figure

from qee.classes.prodist import PRODIST
from qee.enums.voltage_level import VoltageLevel
from qee.enums.voltage_type import VoltageType


class Graph:
    """
    Gera gráficos com valores fornecidos

    Parameters:
        data_frame: data_frame com os valores
        x_key: chave do data_frame para os valores do eixo x
        y_key: chave do data_frame para os valores do eixo y
    """

    def __init__(self, data_frame: DataFrame, x_key: str, y_key: str) -> None:
        self.x_values: Series[float] = data_frame[x_key]
        self.y_values: Series[float] = data_frame[y_key]
        plot: tuple[Figure, Axes] = subplots()
        self.axs: Axes = plot[1]
        self.axs.plot(self.x_values, self.y_values)

    def voltage(self, reference: VoltageType) -> None:
        """
        Destaca os parâmetros para tensão de acordo com o PRODIST

        Parameters:
            reference: tensão de referência

        Returns:
            None

        Raises:
            None

        Examples:
            >>> graph = Graph([1, 2, 3], [1, 4, 9])
            >>> graph.voltage(VoltageType.V220)

        Note:
            None

        Todo:
            None

        """

        prodist = PRODIST()
        cr_sup: int = prodist.get_voltage_range(reference)["cr-sup"]
        ad_sup: int = prodist.get_voltage_range(reference)["ad-sup"]
        ad_inf: int = prodist.get_voltage_range(reference)["ad-inf"]
        cr_inf: int = prodist.get_voltage_range(reference)["cr-inf"]

        self.axs.axhline(
            y=cr_sup,
            color="r",
            linestyle="--",
            label=VoltageLevel.CRITICAL.value,
        )
        # self.axs.axhline(y=ad_sup, color="y", linestyle="--")
        self.axs.axhline(y=reference.value, color="g", linestyle="--")
        # self.axs.axhline(y=ad_inf, color="y", linestyle="--")
        self.axs.axhline(y=cr_inf, color="r", linestyle="--")

        self.axs.axhspan(
            ad_sup,
            cr_sup,
            facecolor="yellow",
            alpha=0.5,
            label=VoltageLevel.PRECARIOUS.value,
        )
        self.axs.axhspan(
            ad_inf,
            ad_sup,
            facecolor="green",
            alpha=0.5,
            label=VoltageLevel.ADEQUATE.value,
        )
        self.axs.axhspan(cr_inf, ad_inf, facecolor="yellow", alpha=0.5)

        # set legends
        # self.axs.legend(loc="upper right")

    def save(self, path: str, image_format: str = "svg") -> None:
        """
        Salva o gráfico

        Parameters:
            path: caminho para salvar o gráfico
            image_format: formato do gráfico (svg, png, etc.)

        Returns:
            None

        Raises:
            None

        Examples:
            >>> graph = Graph([1, 2, 3], [1, 4, 9])
            >>> graph.voltage(VoltageType.V220)
            >>> graph.save("graph.svg")

        Note:
            None

        Todo:
            None
        """

        return savefig(path, format=image_format)

    def show(self) -> None:
        """
        Exibe o gráfico

        Parameters:
            None

        Returns:
            None

        Raises:
            None

        Examples:
            >>> graph = Graph([1, 2, 3], [1, 4, 9])
            >>> graph.voltage(VoltageType.V220)
            >>> graph.show()

        Note:
            None

        Todo:
            None
        """

        return plt_show()
