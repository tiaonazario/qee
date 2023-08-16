"""Define a classificação do tipo de consumidor"""

from enum import Enum


class ConsumerType(Enum):
    """
    Determina o tipo de consumidor atribuindo um nome e um valor

    - BT: Consumidor de Baixa Tensão
    - MT: Consumidor de Média Tensão
    - AT: Consumidor de Alta Tensão
    """

    BT = 'Baixa Tensão'
    MT = 'Média Tensão'
    AT = 'Alta Tensão'
