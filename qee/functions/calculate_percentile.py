"""Modulo de para calculo do percentil"""


def calculate_percentile(values: list[float], percentile: float) -> float:
    """
    Calcula o percentil de um conjunto de valores

    Parameters:
        values: Lista de valores
        percentile: Percentil a ser calculado

    Returns:
        Valor do percentil calculado

    Examples:
        >>> calculate_percentile([1, 2, 3, 4, 5], 50)
        3.0

        >>> calculate_percentile([1, 2, 3, 4, 5], 30)
        1.5
    """

    sorted_values: list[float] = sorted(values)
    size: int = len(sorted_values)
    position: float = (percentile / 100) * (size + 1)

    if position.is_integer():
        return sorted_values[int(position) - 1]

    position_floor: int = int(position)
    position_ceil: int = position_floor + 1
    value_floor: float = sorted_values[position_floor - 1]
    value_ceil: float = sorted_values[position_ceil - 1]
    percentile_value: float = (value_floor + value_ceil) / 2

    return percentile_value
