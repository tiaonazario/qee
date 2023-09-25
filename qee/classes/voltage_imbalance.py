class VoltageImbalance:
    """Desequilíbrio de tensão"""

    def __init__(self, v_ab: float, v_bc: float, v_ca: float) -> None:
        self.v_ab = v_ab
        self.v_bc = v_bc
        self.v_ca = v_ca

    def factor(self) -> float:
        """Calcular o FD%"""

        beta = (self.v_ab**4 + self.v_bc**4 + self.v_ca**4) / (
            (self.v_ab**2 + self.v_bc**2 + self.v_ca**2) ** 2
        )

        numerator = 1 - (3 - 6 * beta) ** (1 / 2)
        denominator = 1 + (3 - 6 * beta) ** (1 / 2)

        value = float(100 * ((numerator / denominator) ** (1 / 2)))

        return value
