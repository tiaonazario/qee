from enum import Enum


class VoltageValue(Enum):
    """Define os nomes e valores para as tensões permitidas"""

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


class VoltageClassify(Enum):
    """Define os nomes e valores para classificação das tensões"""

    ADEQUATE = "Adequada"
    PRECARIOUS = "Precária"
    CRITICAL = "Crítica"


class FrequencyClassify(Enum):
    """Define os nomes e valores para classificação das frequências"""

    ADEQUATE = "Adequada"
    LOW = "Baixa"
    HIGH = "Alta"


class PowerFactorClassify(Enum):
    """Define os nomes e valores para classificação dos fator de potência"""

    ADEQUATE = "Adequada"
    LOW = "Baixo"
