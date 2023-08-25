from qee.classes import Graphic
from qee.enums import VoltageValue


def test_graphic() -> None:
    """Testa o modulo de gerar gráficos"""

    x_values: list[float] = [1, 2, 3, 4]
    y_values: list[float] = [219, 245, 218.5, 198.6]

    graphic = Graphic(x_values, y_values)
    graphic.voltage(VoltageValue.V220)
    graphic.save('data/graphic.svg')
    graphic.show()

    assert graphic
