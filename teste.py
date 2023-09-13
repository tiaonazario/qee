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


# Obtém uma lista dos valores do enum VoltageValue
values_list = [member.value for member in VoltageValue]

# Imprime a lista de valores
print(values_list)
