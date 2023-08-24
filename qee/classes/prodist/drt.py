"""
Modulo DRT

Este módulo contém a definição da classe DRT (Duração Relativa da Transgressão)
utilizada para calcular a Duração Relativa da Transgressão para Tensão Precária e Crítica.

Este módulo pode ser utilizado para criar instâncias da classe DRT e realizar cálculos
relacionados à duração relativa da transgressão em sistemas de tensão elétrica.
"""


class DRT:
    """
    Classe para trabalhar com a Duração Relativa da Transgressão, para Tensão Precária e Crítica

    Parameters:
        drp: Duração relativa da transgressão para tensão precária
        drc: Duração relativa da transgressão para tensão crítica
    """

    def __init__(self, drp: float = 0, drc: float = 0) -> None:
        self.drp: float = drp
        self.drc: float = drc

    def drp_limit(self) -> float:
        """Determina o valor para drp_limit"""
        return 3

    def drc_limit(self) -> float:
        """Determina o valor para drc_limit"""
        return 0.5

    def __str__(self) -> str:
        return f'{{drp: {self.drp:.2f}%, drc: {self.drc:.2f}%}}'
