"""
Modulo Indicadores de Tensão
"""

from .drt import DRT
from .nlt import NLT


class VoltageIndicators:
    """
    Classe para trabalhar com os indicadores de tensão
    """

    def __init__(self, nlt: NLT, drt: DRT) -> None:
        self.nlt = nlt
        self.drt = drt

    def __str__(self) -> str:
        return f'{{nla: {self.nlt.nla}, nlp: {self.nlt.nlp}, nlc: {self.nlt.nlc}, drp: {self.drt.drp:.2f}%, drc: {self.drt.drc:.2f}%}}'
