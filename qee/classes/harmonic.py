"""
Modulo para tratar dos Indicadores de Distorções Harmônicas

|                                **Descrição**                               | **Símbolo** |
|:----------------------------------------------------------------------------------:|:-----------:|
| Distorção harmônica individual de tensão de ordem h                                |    DITh%    |
| Distorção harmônica total de tensão                                                |     DTT%    |
| Distorção harmônica total de tensão para as componentes pares não múltiplas de 3   |    DTTp%    |
| Distorção harmônica total de tensão para as componentes ímpares não múltiplas de 3 |    DTTi%    |
| Distorção harmônica total de tensão para as componentes múltiplas de 3             |    DTT3%    |
| Valor do indicador DTT% que foi superado em apenas 5% das 1.008 leituras válidas   |    DTT95%   |
| Valor do indicador DTTP% que foi superado em apenas 5% das 1.008 leituras válidas  |   DTTp95%   |
| Valor do indicador DTTI% que foi superado em apenas 5% das 1.008 leituras válidas  |   DTTi95%   |
| Valor do indicador DTT3% que foi superado em apenas 5% das 1.008 leituras válidas  |   DTT395%   |
"""


class Harmonic:
    """
    Trabalha os Indicadores de Distorções Harmônicas

    Parameters:
        voltages_h: Lista com tensões harmônicas de ordem h
        fundamental_voltage: Tensão fundamental medida

    Examples:
        >>> harmonic = Harmonic([0.1, 0.2, 0.3], 0.4)
    """

    def __init__(
        self, voltages_h: list[float], fundamental_voltage: float
    ) -> None:
        self.voltages_h: list[float] = voltages_h
        self.fundamental_voltage: float = fundamental_voltage

    def dit_h(self, voltage_h: float) -> float:
        """
        Calcula a Distorção harmônica individual de tensão de ordem h

        Parameters:
            voltage_h: Tensão harmônica de ordem h

        Returns:
            Distorção harmônica individual de tensão de ordem h

        Examples:
            >>> harmonic = Harmonic([0.1, 0.2, 0.3], 0.4)
            >>> harmonic.dit_h(0.2)
            0.2
        """

        return (voltage_h / self.fundamental_voltage) * 100

    def dtt(self) -> float:
        """
        Calcula a Distorção harmônica total de tensão

        Returns:
            Distorção harmônica total de tensão

        Examples:
            >>> harmonic = Harmonic([0.1, 0.2, 0.3], 0.4)
            >>> harmonic.dtt()
            0.6
        """

        sum_: float = 0
        for voltage_h in self.voltages_h:
            sum_ += voltage_h**2

        return self.dit_h(sum_)

    def dtt_p(self) -> float:
        """
        Calcula a Distorção harmônica total de tensão para as componentes pares não múltiplos de 3

        Returns:
            Distorção harmônica total de tensão para as componentes pares não múltiplos de 3

        Examples:
            >>> harmonic = Harmonic([0.1, 0.2, 0.3], 0.4)
            >>> harmonic.dtt_p()
            0.4
        """

        sum_: float = 0
        for i, voltage_h in enumerate(self.voltages_h):
            if i % 2 == 0 and i % 3 != 0:
                sum_ += voltage_h**2

        return self.dit_h(sum_)

    def dtt_i(self) -> float:
        """
        Calcula a Distorção harmônica total de tensão para as componentes ímpares não múltiplos de 3

        Returns:
            Distorção harmônica total de tensão para as componentes ímpares não múltiplos de 3

        Examples:
            >>> harmonic = Harmonic([0.1, 0.2, 0.3], 0.4)
            >>> harmonic.dtt_i()
            0.4
        """

        sum_: float = 0
        for i, voltage_h in enumerate(self.voltages_h):
            if i % 2 != 0 and i % 3 != 0:
                sum_ += voltage_h**2

        return self.dit_h(sum_)

    def dtt_3(self) -> float:
        """
        Calcula a Distorção harmônica total de tensão para as componentes múltiplos de 3

        Returns:
            Distorção harmônica total de tensão para as componentes múltiplos de 3

        Examples:
            >>> harmonic = Harmonic([0.1, 0.2, 0.3], 0.4)
            >>> harmonic.dtt_3()
            0.4
        """

        sum_: float = 0
        for i, voltage_h in enumerate(self.voltages_h):
            if i % 3 == 0:
                sum_ += voltage_h**2

        return self.dit_h(sum_)
