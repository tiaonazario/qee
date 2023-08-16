"""Define os valores de níveis de tensão"""

from enum import Enum


class VoltageLevel(Enum):
    """
    Define os nomes e valores para as respectivos níveis de tensão

    - CRITICAL: Nível de tensão crítico.
    - ADEQUATE: Nível de tensão adequado.
    - PRECARIOUS: Nível de tensão precária.
    """

    CRITICAL = 'Crítica'
    ADEQUATE = 'Adequada'
    PRECARIOUS = 'Precária'
