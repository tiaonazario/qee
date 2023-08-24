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
