import pandas as pd
import numpy as np

from tabulate import tabulate

from qee.analysis.graphic import Graphic
from qee.analysis.harmonics import Harmonics
from qee.analysis.voltage import Voltage
from qee.analysis.voltage_variation import VoltageVariation
from qee.enums import VoltageValue, VoltageClassify
from qee.constants import prodist


class Analysis:
    """Elabora a analise da Qualidade de Energia Elétrica (QEE)"""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def graphic_voltage(
        self, voltages: list[list[str | VoltageValue]]
    ) -> None:
        """Gera o gráfico para as tensões"""

        x_axis = list(range(1, 1009))

        for voltage in voltages:
            label = voltage[0]
            reference = voltage[1]

            y_axis: list[float] = self.data[label].to_list()

            filename = f"{label.replace(' ', '_')}.png"

            graphic = Graphic(x_axis, y_axis)
            graphic.voltage(reference)
            graphic.save(f"waves/{filename}")

    def voltage_variation(self, voltages: list[list[str | VoltageValue]]):
        """Calcula a variação da tensão"""

        for voltage in voltages:
            label = voltage[0]
            reference = voltage[1]

            values: list[float] = self.data[label].to_list()

            variation = VoltageVariation(values, reference)
            indicators = variation.indicators()

            print(label.center(40))
            data = {
                "Indicador": ["DRP", "DRC"],
                "Obtido": [
                    f"{indicators[0]:.2f}%",
                    f"{indicators[1]:.2f}%",
                ],
                "PRODIST": [
                    f"{prodist.DRP_LIMIT:.2f}%",
                    f"{prodist.DRC_LIMIT:.2f}%",
                ],
            }
            print(tabulate(data, headers="keys", tablefmt="fancy_grid"))

    def harmonics(self, voltage_labels: list[list[str | list[str]]]):
        """Calcula os indicadores de distorções de harmônicas"""

        for voltage_label in voltage_labels:
            total_harmonic_distortions = []
            total_harmonic_distortions_even = []
            total_harmonic_distortions_odd = []
            total_harmonic_distortions_3 = []

            label: str = voltage_label[0]
            harmonic_labels: list[str] = voltage_label[1]

            harmonic_voltages = self.data[harmonic_labels]
            for values in harmonic_voltages.values.tolist():
                distortion = Harmonics(values)
                indicators = distortion.harmonic_distortion()

                total_harmonic_distortions.append(indicators[0])
                total_harmonic_distortions_even.append(indicators[1])
                total_harmonic_distortions_odd.append(indicators[2])
                total_harmonic_distortions_3.append(indicators[3])

            indicators_95 = [
                float(np.percentile(total_harmonic_distortions, 95)),
                float(np.percentile(total_harmonic_distortions_even, 95)),
                float(np.percentile(total_harmonic_distortions_odd, 95)),
                float(np.percentile(total_harmonic_distortions_3, 95)),
            ]

            print(label.center(40))
            data = {
                "Indicador": ["DTT_95", "DTT_p_95", "DTT_i_95", "DTT_3_95"],
                "Obtido": [
                    f"{indicators_95[0]:.2f}%",
                    f"{indicators_95[1]:.2f}%",
                    f"{indicators_95[2]:.2f}%",
                    f"{indicators_95[3]:.2f}%",
                ],
                "PRODIST": [
                    f"{prodist.DTT_95:.2f}%",
                    f"{prodist.DTT_P_95:.2f}%",
                    f"{prodist.DTT_I_95:.2f}%",
                    f"{prodist.DTT_3_95:.2f}%",
                ],
            }
            print(tabulate(data, headers="keys", tablefmt="fancy_grid"))
