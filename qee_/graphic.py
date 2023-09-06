from matplotlib.figure import Figure
from matplotlib.pyplot import Axes, savefig, figure, gca
from matplotlib.pyplot import show as plt_show

from qee.prodist.prodist import PRODIST
from qee.enums.voltage_type import VoltageType
from qee.enums.voltage_value import VoltageValue

from qee.utils.get_file_extension import get_file_extension


class Graphic:
    """
    Gera gráficos com valores fornecidos
    """

    def __init__(self, x_values: list[float], y_values: list[float]) -> None:
        self.x_values: list[float] = x_values
        self.y_values: list[float] = y_values

        # plot: tuple[Figure, Axes] = subplots()
        self.figure: Figure = figure(figsize=(16, 9))
        self.axes: Axes = gca()

        self.axes.plot(self.x_values, self.y_values)

    def voltage(self, reference: VoltageValue) -> None:
        """
        Destaca os parâmetros para tensão de acordo com o PRODIST
        """

        prodist = PRODIST()
        voltage_range = prodist.voltage_range()
        cr_sup: int = voltage_range.get_one(reference)["cr-sup"]
        ad_sup: int = voltage_range.get_one(reference)["ad-sup"]
        ad_inf: int = voltage_range.get_one(reference)["ad-inf"]
        cr_inf: int = voltage_range.get_one(reference)["cr-inf"]

        self.axes.axhline(
            y=cr_sup,
            color="r",
            linestyle="--",
            label=VoltageType.CRITICAL.value,
        )
        # self.axes.axhline(y=ad_sup, color="y", linestyle="--")
        self.axes.axhline(y=reference.value, color="g", linestyle="--")
        # self.axes.axhline(y=ad_inf, color="y", linestyle="--")
        self.axes.axhline(y=cr_inf, color="r", linestyle="--")

        self.axes.axhspan(
            ad_sup,
            cr_sup,
            facecolor="yellow",
            alpha=0.5,
            label=VoltageType.PRECARIOUS.value,
        )
        self.axes.axhspan(
            ad_inf,
            ad_sup,
            facecolor="green",
            alpha=0.5,
            label=VoltageType.ADEQUATE.value,
        )
        self.axes.axhspan(cr_inf, ad_inf, facecolor="yellow", alpha=0.5)

        # set legends
        self.axes.legend(loc="upper right")

    def save(self, path: str) -> None:
        """
        Salva o gráfico como uma imagem
        """

        return savefig(path, format=get_file_extension(path), transparent=True)

    def show(self) -> None:
        """
        Exibe o gráfico
        """

        return plt_show()
