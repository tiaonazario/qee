"""Define os valores de tensão permitidos"""
from enum import IntEnum, unique


@unique
class VoltageValue(IntEnum):
    """
    Define os nomes e valores para as respectivas tensões permitidas

    - V110: Tensão elétrica de 110 volts.
    - V120: Tensão elétrica de 120 volts.
    - V127: Tensão elétrica de 127 volts.
    - V208: Tensão elétrica de 208 volts.
    - V215: Tensão elétrica de 215 volts.
    - V220: Tensão elétrica de 220 volts.
    - V230: Tensão elétrica de 230 volts.
    - V240: Tensão elétrica de 240 volts.
    - V254: Tensão elétrica de 254 volts.
    - V380: Tensão elétrica de 380 volts.
    - V440: Tensão elétrica de 440 volts.
    """

    V110 = 110
    V120 = 120
    V127 = 127
    V208 = 208
    V215 = 215
    V220 = 220
    V230 = 230
    V240 = 240
    V254 = 254
    V380 = 380
    V440 = 440
