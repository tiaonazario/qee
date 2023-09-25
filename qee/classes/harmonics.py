from typing import Literal


class Harmonics:
    """Trabalha com os indicadores de distorções harmônicas"""

    def __init__(self, voltages: list[float]) -> None:
        self.voltages = voltages
        self.fundamental = abs(voltages[0])

    def individual_harmonic_distortion(self, voltage: float) -> float:
        """Calcula a Distorção harmônica individual de tensão de ordem h"""

        return (voltage / self.fundamental) * 100

    def distortion(
        self,
    ) -> dict[Literal["DTT", "DTTp", "DTTi", "DTT3"], float]:
        """Calcula as Distorção harmônicas total de tensão"""

        total_sum: float = 0
        total_sum_even_not_multiple_3: float = 0
        total_sum_odd_not_multiple_3: float = 0
        total_sum_multiple_3: float = 0

        for index, voltage in enumerate(self.voltages):
            order = index + 1

            if order >= 2:
                total_sum += voltage**2

            if order % 2 == 0 and order % 3 != 0:
                total_sum_even_not_multiple_3 += voltage**2

            if order >= 5 and order % 2 != 0 and order % 3 != 0:
                total_sum_odd_not_multiple_3 += voltage**2

            if order % 3 == 0:
                total_sum_multiple_3 += voltage**2

        return {
            "DTT": self.individual_harmonic_distortion(total_sum ** (1 / 2)),
            "DTTp": self.individual_harmonic_distortion(
                total_sum_even_not_multiple_3 ** (1 / 2)
            ),
            "DTTi": self.individual_harmonic_distortion(
                total_sum_odd_not_multiple_3 ** (1 / 2)
            ),
            "DTT3": self.individual_harmonic_distortion(
                total_sum_multiple_3 ** (1 / 2)
            ),
        }
