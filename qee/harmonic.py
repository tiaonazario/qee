class Harmonic:
    """
    Trabalha os Indicadores de Distorções Harmônicas
    """

    def __init__(
        self, voltages_h: list[float], fundamental_voltage: float
    ) -> None:
        self.voltages_h: list[float] = voltages_h
        self.fundamental_voltage: float = abs(fundamental_voltage)

    def dit_h(self, voltage_h: float) -> float:
        """
        Calcula a Distorção harmônica individual de tensão de ordem h
        """

        return (voltage_h / self.fundamental_voltage) * 100

    def dtt(self) -> float:
        """
        Calcula a Distorção harmônica total de tensão
        """

        summation: float = 0
        for index, voltage_h in enumerate(self.voltages_h):
            order: int = index + 1
            if order >= 2:
                summation += voltage_h**2

        return self.dit_h(summation ** (1 / 2))

    def dtt_p(self) -> float:
        """
        Calcula a Distorção harmônica total de tensão para as componentes pares não múltiplos de 3
        """

        summation: float = 0
        for index, voltage_h in enumerate(self.voltages_h):
            order: int = index + 1
            if order % 2 == 0 and order % 3 != 0:
                summation += voltage_h**2

        return self.dit_h(summation ** (1 / 2))

    def dtt_i(self) -> float:
        """
        Calcula a Distorção harmônica total de tensão para as componentes ímpares não múltiplos de 3
        """

        summation: float = 0
        for index, voltage_h in enumerate(self.voltages_h):
            order: int = index + 1
            if order >= 5 and order % 2 != 0 and order % 3 != 0:
                summation += voltage_h**2

        return self.dit_h(summation ** (1 / 2))

    def dtt_3(self) -> float:
        """
        Calcula a Distorção harmônica total de tensão para as componentes múltiplos de 3
        """

        summation: float = 0
        for index, voltage_h in enumerate(self.voltages_h):
            order: int = index + 1
            if order % 3 == 0:
                summation += voltage_h**2

        return self.dit_h(summation ** (1 / 2))
