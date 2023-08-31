class IndicatorsDH:
    """Distorções harmônicas"""

    def __init__(
        self, dtt_95: float, dtt_p_95: float, dtt_i_95: float, dtt_3_95: float
    ) -> None:
        self.dtt_95 = dtt_95
        self.dtt_p_95 = dtt_p_95
        self.dtt_i_95 = dtt_i_95
        self.dtt_3_95 = dtt_3_95

    def to_dict(self) -> dict[str, float]:
        """Converter os parâmetros da classe em um dicionário"""

        return {
            "dtt_95": self.dtt_95,
            "dtt_p_95": self.dtt_p_95,
            "dtt_i_95": self.dtt_i_95,
            "dtt_3_95": self.dtt_3_95,
        }

    def __str__(self) -> str:
        return str(self.to_dict())
