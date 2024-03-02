import numpy as np
import pandas as pd

from qee.classes.frequency import Frequency
from qee.classes.harmonics import Harmonics
from qee.classes.power_factor import PowerFactor
from qee.classes.voltage_imbalance import VoltageImbalance
from qee.classes.voltage_variation import VoltageVariation
from qee.constants import prodist
from qee.types import VoltageValueType


class Analysis:
    """Elabora a analise da Qualidade de Energia Elétrica (QEE)"""

    def __init__(self, data_frame: pd.DataFrame) -> None:
        self.data_frame = data_frame

    def voltage_variation(
        self, labels: list[str], reference: VoltageValueType
    ) -> pd.DataFrame:
        """Calcula a variação de tensão"""

        drp_list: list[tuple[str, float]] = []
        drc_list: list[tuple[str, float]] = []

        for label in labels:
            values: list[float] = self.data_frame[label].to_list()

            indicators = VoltageVariation(values, reference).indicators()

            drp_list.append((label, indicators['DRP']))
            drc_list.append((label, indicators['DRC']))

        # drp_selected =
        # drc_selected =
        drp_label, drp = max(drp_list, key=lambda x: x[1])
        drc_label, drc = max(drc_list, key=lambda x: x[1])

        data = {
            'Indicador': ['DRP', 'DRC'],
            'Tensão': [drp_label, drc_label],
            'Obtido': [f'{drp:.2f}%', f'{drc:.2f}%'],
            'PRODIST': [
                f'{prodist.DRP_LIMIT:.2f}%',
                f'{prodist.DRC_LIMIT:.2f}%',
            ],
        }

        return pd.DataFrame(data)

    def harmonics(self, labels: list[str]) -> pd.DataFrame:
        """Calcula os indicadores de distorções de harmônicas"""

        total_harmonic_distortions = []
        total_harmonic_distortions_even = []
        total_harmonic_distortions_odd = []
        total_harmonic_distortions_3 = []

        harmonic_voltages = self.data_frame[labels]
        for values in harmonic_voltages.values.tolist():
            indicators = Harmonics(values).distortion()

            total_harmonic_distortions.append(indicators['DTT'])
            total_harmonic_distortions_even.append(indicators['DTTp'])
            total_harmonic_distortions_odd.append(indicators['DTTi'])
            total_harmonic_distortions_3.append(indicators['DTT3'])

        dtt_95, dtt_p_95, dtt_i_95, dtt_3_95 = [
            float(np.percentile(total_harmonic_distortions, 95)),
            float(np.percentile(total_harmonic_distortions_even, 95)),
            float(np.percentile(total_harmonic_distortions_odd, 95)),
            float(np.percentile(total_harmonic_distortions_3, 95)),
        ]

        data = {
            'Indicador': [
                'DTT_95%',
                'DTT_p_95%',
                'DTT_i_95%',
                'DTT_3_95%',
            ],
            'Obtido': [
                f'{dtt_95:.2f}%',
                f'{dtt_p_95:.2f}%',
                f'{dtt_i_95:.2f}%',
                f'{dtt_3_95:.2f}%',
            ],
            'PRODIST': [
                f'{prodist.DTT_95:.2f}%',
                f'{prodist.DTT_P_95:.2f}%',
                f'{prodist.DTT_I_95:.2f}%',
                f'{prodist.DTT_3_95:.2f}%',
            ],
        }

        return pd.DataFrame(data)

    def power_factor(self, label: str) -> pd.DataFrame:
        """Analisa o fator de potência"""

        fps: list[float] = self.data_frame[label].to_list()

        amount_low = 0
        amount_adequate = 0
        for factor in fps:
            classify = PowerFactor(factor).classify()
            if classify == 'Adequado':
                amount_adequate += 1
            else:
                amount_low += 1

        data = {
            'Classificação': ['Adequado', 'Crítico'],
            'Quantidade': [str(amount_adequate), str(amount_low)],
        }

        return pd.DataFrame(data)

    def voltage_imbalance(self, labels: list[str]) -> pd.DataFrame:
        """Calcula o desequilíbrio de tensão"""

        values = self.data_frame[labels]

        indicators: list[float] = []
        for voltages in values.values.tolist():
            imbalance = VoltageImbalance(voltages[0], voltages[1], voltages[2])
            indicators.append(imbalance.factor())

        indicator_95 = float(np.percentile(indicators, 95))

        data = {
            'Indicador': ['FD95%'],
            'Obtido': [f'{indicator_95:.2f}%'],
            'PRODIST': [f'{prodist.FD_LIMIT:.2f}%'],
        }

        return pd.DataFrame(data)

    def flicker(self, label: str) -> pd.DataFrame:
        """Calcula o flicker"""

        psts: list[float] = self.data_frame[label].to_list()

        pst_95 = float(np.percentile(psts, 95))

        data = {
            'Indicador': ['Pst95%'],
            'Obtido': [f'{pst_95:.2f}pu'],
            'PRODIST': [f'{prodist.P_ST_LIMIT:.2f}pu'],
        }

        return pd.DataFrame(data)

    def frequency_variation(self, label: str) -> pd.DataFrame:
        """Calcula a variação de frequência"""

        frequencies: list[float] = self.data_frame[label].to_list()

        low = 0
        high = 0
        adequate = 0
        for frequency in frequencies:
            classify = Frequency(frequency).classify()
            if classify == 'Adequada':
                adequate += 1
            elif classify == 'Baixa':
                low += 1
            else:
                high += 1

        data = {
            'Classificação': ['Alta', 'Adequada', 'Baixa'],
            'Quantidade': [str(high), str(adequate), str(low)],
            'Porção': [
                f'{(high / 1008) * 100:.2f}%',
                f'{(adequate / 1008) * 100:.2f}%',
                f'{(low / 1008) * 100:.2f}%',
            ],
        }

        return pd.DataFrame(data)
