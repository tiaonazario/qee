from qee.functions import calculate_percentile


def test_calculate_percentile() -> None:
    """Testa o calculo do percentil"""

    assert calculate_percentile([1, 2, 3, 4, 5], 50) == 3
    assert calculate_percentile([1, 2, 3, 4, 5], 30) == 1.5
