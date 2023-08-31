class DRT:
    """
    Classe para trabalhar com a Duração Relativa da Transgressão, para Tensão Precária e Crítica
    """

    def __init__(self, drp: float, drc: float) -> None:
        self.drp = drp
        self.drc = drc

    def to_dict(self) -> dict[str, float]:
        """Transforma a classe em um dicionário"""

        return {"drp": self.drp, "drc": self.drc}

    def __str__(self) -> str:
        return str(self.to_dict())
