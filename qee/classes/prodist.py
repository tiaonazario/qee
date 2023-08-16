"""Esse modulo define a classe PRODIST"""

from qee.enums.voltage_type import VoltageType


class PRODIST:
    """
    Define faixa de variação de tensão de leitura fornecida pelo PRODIST

    Parameters:
        None

    Returns:
        None
    """

    def __init__(self) -> None:
        self._vvr: dict[int, dict[str, int]] = self.voltage_ranges()

    def voltage_ranges(self) -> dict[int, dict[str, int]]:
        """
        Define faixa de variação de tensão de leitura fornecida pelo PRODIST

        Parameters:
            None

        Returns:
            dict[int, dict[str, int]]: faixa de variação de tensão de leitura
        """

        return {
            110: {
                "cr-sup": 117,
                "ad-sup": 116,
                "ad-inf": 101,
                "cr-inf": 96,
            },
            120: {
                "cr-sup": 127,
                "ad-sup": 126,
                "ad-inf": 110,
                "cr-inf": 104,
            },
            127: {
                "cr-sup": 135,
                "ad-sup": 133,
                "ad-inf": 117,
                "cr-inf": 110,
            },
            208: {
                "cr-sup": 220,
                "ad-sup": 218,
                "ad-inf": 191,
                "cr-inf": 181,
            },
            215: {
                "cr-sup": 122,
                "ad-sup": 121,
                "ad-inf": 106,
                "cr-inf": 100,
            },
            220: {
                "cr-sup": 233,
                "ad-sup": 231,
                "ad-inf": 202,
                "cr-inf": 191,
            },
            230: {
                "cr-sup": 244,
                "ad-sup": 242,
                "ad-inf": 212,
                "cr-inf": 200,
            },
            240: {
                "cr-sup": 254,
                "ad-sup": 252,
                "ad-inf": 221,
                "cr-inf": 209,
            },
            254: {
                "cr-sup": 269,
                "ad-sup": 267,
                "ad-inf": 234,
                "cr-inf": 221,
            },
            380: {
                "cr-sup": 403,
                "ad-sup": 399,
                "ad-inf": 350,
                "cr-inf": 331,
            },
            440: {
                "cr-sup": 466,
                "ad-sup": 462,
                "ad-inf": 405,
                "cr-inf": 383,
            },
        }

    def get_voltage_range(self, voltage_type: VoltageType) -> dict[str, int]:
        """
        Determina a Faixa de Variação da Tensão de Leitura

        Parameters:
            voltage: Tensão de Leitura.

        Returns:
            Faixa de Variação da Tensão de Leitura.

        Examples:
            >>> self.get_voltage_range(110)
            {'cr-sup': 117, 'ad-sup': 116, 'ad-inf': 101, 'cr-inf': 96 }

            >>> self.get_voltage_range(120)
            {'cr-sup': 127, 'ad-sup': 126, 'ad-inf': 110, 'cr-inf': 104 }
        """

        return self._vvr[voltage_type.value]