from typing import List, Tuple

import numpy as np
import pandas as pd
from tabulate import tabulate

from qee.analysis.frequency import Frequency
from qee.analysis.graphic import Graphic
from qee.analysis.harmonics import Harmonics
from qee.analysis.power_factor import PowerFactor
from qee.analysis.voltage import Voltage
from qee.analysis.voltage_imbalance import VoltageImbalance
from qee.analysis.voltage_variation import VoltageVariation
from qee.constants import prodist
from qee.enums import (
    FrequencyClassify,
    VoltageClassify,
    VoltageValue,
    PowerFactorClassify,
)
from qee.pdf import PDF


class Analysis:
    """Elabora a analise da Qualidade de Energia Elétrica (QEE)"""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data
        self.pdf = PDF()
        self.pdf.add_title("Relatório de Análise de QEE")

    def build_table(self, filename: str):
        """Construir tabela"""

        self.pdf.build(filename)
        print("Tabela construída com sucesso!")

    def graphic_voltage(
        self, label: str, reference: VoltageValue, extension: str = "png"
    ) -> None:
        """Gera o gráfico para as tensões"""

        x_axis: list[float] = list(range(1, 1009))
        y_axis: list[float] = self.data[label].to_list()

        filename = f"{label.replace(' ', '_')}.{extension}"

        graphic = Graphic(x_axis, y_axis)
        graphic.voltage(reference)
        graphic.save(f"waves/{filename}")

    def voltage_variation(
        self,
        labels: list[str],
        reference: VoltageValue,
        print_table: bool = False,
        pdf_table: bool = False,
    ) -> pd.DataFrame:
        """Calcula a variação da tensão"""

        drp_list = []
        drc_list = []

        for label in labels:
            values: list[float] = self.data[label].to_list()

            indicators = VoltageVariation(values, reference).indicators()

            drp_list.append([label, indicators[0]])
            drc_list.append([label, indicators[1]])

        drp_label, drp = max(drp_list, key=lambda x: x[1])
        drc_label, drc = max(drc_list, key=lambda x: x[1])

        data = {
            "Indicador": ["DRP", "DRC"],
            "Tensão": [drp_label, drc_label],
            "Obtido": [f"{drp:.2f}%", f"{drc:.2f}%"],
            "PRODIST": [
                f"{prodist.DRP_LIMIT:.2f}%",
                f"{prodist.DRC_LIMIT:.2f}%",
            ],
        }

        data_frame = pd.DataFrame(data)

        if print_table:
            print("Variação de tensão".center(50))
            print(tabulate(data, headers="keys", tablefmt="fancy_grid"))

        if pdf_table:
            self.pdf.add_subtitle("Variação de tensão")
            table = self.pdf.create_table(
                data_frame.columns.to_list(),
                data_frame.values,
            )
            self.pdf.add(table)
            self.pdf.add_spacer()

        return data_frame

    def harmonics(
        self,
        harmonic_labels: list[str],
        print_table: bool = False,
        pdf_table: bool = False,
    ) -> pd.DataFrame:
        """Calcula os indicadores de distorções de harmônicas"""

        total_harmonic_distortions = []
        total_harmonic_distortions_even = []
        total_harmonic_distortions_odd = []
        total_harmonic_distortions_3 = []

        harmonic_voltages = self.data[harmonic_labels]
        for values in harmonic_voltages.values.tolist():
            distortion = Harmonics(values)
            indicators = distortion.harmonic_distortion()

            total_harmonic_distortions.append(indicators[0])
            total_harmonic_distortions_even.append(indicators[1])
            total_harmonic_distortions_odd.append(indicators[2])
            total_harmonic_distortions_3.append(indicators[3])

        dtt_95, dtt_p_95, dtt_i_95, dtt_3_95 = [
            float(np.percentile(total_harmonic_distortions, 95)),
            float(np.percentile(total_harmonic_distortions_even, 95)),
            float(np.percentile(total_harmonic_distortions_odd, 95)),
            float(np.percentile(total_harmonic_distortions_3, 95)),
        ]

        data = {
            "Indicador": [
                "DTT_95",
                "DTT_p_95",
                "DTT_i_95",
                "DTT_3_95",
            ],
            "Obtido": [
                f"{dtt_95:.2f}%",
                f"{dtt_p_95:.2f}%",
                f"{dtt_i_95:.2f}%",
                f"{dtt_3_95:.2f}%",
            ],
            "PRODIST": [
                f"{prodist.DTT_95:.2f}%",
                f"{prodist.DTT_P_95:.2f}%",
                f"{prodist.DTT_I_95:.2f}%",
                f"{prodist.DTT_3_95:.2f}%",
            ],
        }

        data_frame = pd.DataFrame(data)

        if print_table:
            print("Distorções harmônicas".center(40))
            print(tabulate(data, headers="keys", tablefmt="fancy_grid"))

        if pdf_table:
            self.pdf.add_subtitle("Distorções harmônicas")
            table = self.pdf.create_table(
                data_frame.columns.to_list(), data_frame.values
            )
            self.pdf.add(table)
            self.pdf.add_spacer()

        return data_frame

    def voltage_imbalance(
        self,
        labels: list[str],
        print_table: bool = False,
        pdf_table: bool = False,
    ) -> pd.DataFrame:
        """Calcula o desequilíbrio de tensão"""

        values = self.data[labels]

        indicators = []
        for voltages in values.values.tolist():
            imbalance = VoltageImbalance(voltages[0], voltages[1], voltages[2])
            indicators.append(imbalance.factor())

        indicator_95 = float(np.percentile(indicators, 95))

        data = {
            "Indicador": ["FD_95"],
            "Obtido": [f"{indicator_95:.2f}%"],
            "PRODIST": [f"{prodist.FD_LIMIT:.2f}%"],
        }

        data_frame = pd.DataFrame(data)

        if print_table:
            print("Desequilíbrio de tensão".center(40))
            print(tabulate(data, headers="keys", tablefmt="fancy_grid"))

        if pdf_table:
            self.pdf.add_subtitle("Desequilíbrio de tensão")
            table = self.pdf.create_table(
                data_frame.columns.to_list(), data_frame.values
            )
            self.pdf.add(table)
            self.pdf.add_spacer()

        return data_frame

    def frequency_variation(
        self, label: str, print_table: bool = False, pdf_table: bool = False
    ) -> pd.DataFrame:
        """Calcula a variação de frequência"""

        frequencies: list[float] = self.data[label].to_list()

        amount_low = 0
        amount_high = 0
        amount_adequate = 0
        for frequency in frequencies:
            classify = Frequency(frequency).classify()
            if classify == FrequencyClassify.ADEQUATE:
                amount_adequate += 1
            elif classify == FrequencyClassify.LOW:
                amount_low += 1
            else:
                amount_high += 1

        data = {
            "Classificação": [
                FrequencyClassify.LOW.value,
                FrequencyClassify.HIGH.value,
                FrequencyClassify.ADEQUATE.value,
            ],
            "Quantidade": [
                str(amount_low),
                str(amount_high),
                str(amount_adequate),
            ],
        }

        data_frame = pd.DataFrame(data)

        if print_table:
            print("Variação de frequência".center(40))
            print(tabulate(data, headers="keys", tablefmt="fancy_grid"))

        if pdf_table:
            self.pdf.add_subtitle("Variação de frequência")
            table = self.pdf.create_table(
                data_frame.columns.to_list(), data_frame.values
            )
            self.pdf.add(table)

        return data_frame

    def power_factor(
        self, label: str, print_table: bool = False
    ) -> pd.DataFrame:
        """Analise o fator de potência"""

        fps: list[float] = self.data[label].to_list()

        amount_low = 0
        amount_adequate = 0
        for factor in fps:
            classify = PowerFactor(factor).classify()
            if classify == PowerFactorClassify.ADEQUATE:
                amount_adequate += 1
            else:
                amount_low += 1

        data = {
            "Classificação": [
                PowerFactorClassify.ADEQUATE.value,
                PowerFactorClassify.LOW.value,
            ],
            "Quantidade": [
                str(amount_adequate),
                str(amount_low),
            ],
        }

        data_frame = pd.DataFrame(data)

        if print_table:
            print("Fator de potência".center(40))
            print(tabulate(data, headers="keys", tablefmt="fancy_grid"))

        return data_frame
