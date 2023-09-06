class VoltageImbalance:
    """Classe para trabalhar com o desequilíbrio de tensão"""

    def __init__(self, v_ab: float, v_bc: float, v_ca: float) -> None:
        self.v_ab = v_ab
        self.v_bc = v_bc
        self.v_ca = v_ca

    def beta(self) -> float:
        """Calcular do beta para obtenção do FD%"""

        return (self.v_ab**4 + self.v_bc**4 + self.v_ca**4) / (
            (self.v_ab**2 + self.v_bc**2 + self.v_ca**2) ** 2
        )

    def factor(self) -> float:
        """Calcular o FD%"""

        beta = self.beta()

        return 100 * (
            ((1 - (3 - 6 * beta) ** (1 / 2)) / (1 + (3 - 6 * beta) ** (1 / 2)))
            ** (1 / 2)
        )
