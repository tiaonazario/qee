import matplotlib.pyplot as plt

from qee.constants import prodist
from qee.types import VoltageClassifyType, VoltageValueType


class Graphic:
    """Gera o gráfico para valores fornecidos"""

    def __init__(
        self, x_values: list[float], y_values: list[float], title: str
    ) -> None:
        self.x_values = x_values
        self.y_values = y_values

        self.figure = plt.figure(figsize=(8, 4.5))
        self.axes: plt.Axes = plt.gca()

        self.axes.set_title(title)

        self.axes.plot(self.x_values, self.y_values)

    def voltage(self, reference: VoltageValueType) -> None:
        """Destaca os parâmetros para tensão de acordo com o PRODIST"""

        voltage_range = prodist.VOLTAGE_RANGE[reference]

        cr_sup = voltage_range['cr-sup']
        ad_sup = voltage_range['ad-sup']
        ad_inf = voltage_range['ad-inf']
        cr_inf = voltage_range['cr-inf']

        ad_label: VoltageClassifyType = 'Adequada'
        cr_label: VoltageClassifyType = 'Crítica'
        pr_label: VoltageClassifyType = 'Precária'

        self.axes.axhline(y=cr_sup, color='r', linestyle='--', label=cr_label)
        self.axes.axhline(y=reference, color='g', linestyle='--')
        self.axes.axhline(y=cr_inf, color='r', linestyle='--')
        self.axes.axhspan(
            ad_sup, cr_sup, facecolor='yellow', alpha=0.3, label=pr_label
        )
        self.axes.axhspan(
            ad_inf, ad_sup, facecolor='green', alpha=0.3, label=ad_label
        )
        self.axes.axhspan(cr_inf, ad_inf, facecolor='yellow', alpha=0.3)

        self.axes.set_xlim(1, 1008)

    def save(self, filepath: str) -> None:
        """Salva o gráfico"""
        extension = filepath.split('.')[-1]

        self.figure.savefig(filepath, format=extension, transparent=True)

        print(f'Gráfico salvo em: {filepath}')

    def show(self) -> None:
        """Exibe o gráfico"""

        plt.show()
