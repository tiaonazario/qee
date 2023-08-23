"""Classe para geração de gráficos"""
# pyright: reportUnknownVariableType=none
# pyright: reportUnknownMemberType=none

from matplotlib.figure import Figure
from matplotlib.pyplot import Axes, savefig
from matplotlib.pyplot import show as plt_show
from matplotlib.pyplot import subplots

from qee.classes.prodist import VoltageRange
from qee.enums.voltage_type import VoltageType
from qee.enums.voltage_value import VoltageValue


class Graphic:
    """
    Gera gráficos com valores fornecidos

    Parameters:
        x_values: valores do eixo x
        y_values: valores do eixo y
    """

    def __init__(self, x_values: list[float], y_values: list[float]) -> None:
        self.x_values: list[float] = x_values
        self.y_values: list[float] = y_values
        plot: tuple[Figure, Axes] = subplots()
        self.axs: Axes = plot[1]
        self.axs.plot(self.x_values, self.y_values)

    def voltage(self, reference: VoltageValue) -> None:
        """
        Destaca os parâmetros para tensão de acordo com o PRODIST

        Parameters:
            reference: tensão de referência

        Returns:
            None

        Examples:
            >>> graph = Graph([1, 2, 3], [1, 4, 9])
            >>> graph.voltage(VoltageValue.V220)

        """

        prodist = VoltageRange()
        cr_sup: int = prodist.get_one(reference)['cr-sup']
        ad_sup: int = prodist.get_one(reference)['ad-sup']
        ad_inf: int = prodist.get_one(reference)['ad-inf']
        cr_inf: int = prodist.get_one(reference)['cr-inf']

        self.axs.axhline(
            y=cr_sup,
            color='r',
            linestyle='--',
            label=VoltageType.CRITICAL.value,
        )
        # self.axs.axhline(y=ad_sup, color="y", linestyle="--")
        self.axs.axhline(y=reference.value, color='g', linestyle='--')
        # self.axs.axhline(y=ad_inf, color="y", linestyle="--")
        self.axs.axhline(y=cr_inf, color='r', linestyle='--')

        self.axs.axhspan(
            ad_sup,
            cr_sup,
            facecolor='yellow',
            alpha=0.5,
            label=VoltageType.PRECARIOUS.value,
        )
        self.axs.axhspan(
            ad_inf,
            ad_sup,
            facecolor='green',
            alpha=0.5,
            label=VoltageType.ADEQUATE.value,
        )
        self.axs.axhspan(cr_inf, ad_inf, facecolor='yellow', alpha=0.5)

        # set legends
        # self.axs.legend(loc="upper right")

    def save(self, path: str, image_format: str = 'svg') -> None:
        """
        Salva o gráfico

        Parameters:
            path: caminho para salvar o gráfico
            image_format: formato do gráfico (svg, png, etc.)

        Returns:
            None

        Examples:
            >>> graph = Graph([1, 2, 3], [1, 4, 9])
            >>> graph.voltage(VoltageValue.V220)
            >>> graph.save("graph.svg")
        """

        return savefig(path, format=image_format)

    def show(self) -> None:
        """
        Exibe o gráfico

        Returns:
            None

        Examples:
            >>> graph = Graph([1, 2, 3], [1, 4, 9])
            >>> graph.voltage(VoltageValue.V220)
            >>> graph.show()
        """

        return plt_show()
