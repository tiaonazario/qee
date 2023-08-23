"""Define os valores de níveis de tensão"""

from enum import StrEnum


class VoltageType(StrEnum):
    """
    Define os nomes e valores para as respectivos níveis de tensão

    - CRITICAL: Nível de tensão crítico.
    - ADEQUATE: Nível de tensão adequado.
    - PRECARIOUS: Nível de tensão precária.
    """

    CRITICAL = 'Crítica'
    ADEQUATE = 'Adequada'
    PRECARIOUS = 'Precária'
