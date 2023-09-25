def get_ext(filename: str) -> str:
    """Retorna a extensão do arquivo"""

    return filename.split('.')[-1]


def harmonic_labels(
    amount: int, prefix: str = '', suffix: str = ''
) -> list[str]:
    """Retorna uma lista com os nomes das colunas de acordo com uma tensão"""

    labels: list[str] = []
    for value in range(1, amount + 1):
        order = str(value).zfill(2)
        labels.append(f'{prefix}{order}{suffix}')

    return labels
