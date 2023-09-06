def get_ext(filename: str) -> str:
    """Retorna a extensão do arquivo"""

    return filename.split(".")[-1]


def harmonic_labels(voltage: str, mode: str, number: int) -> list[str]:
    """Retorna uma lista com os nomes das colunas de acordo com uma tensão"""

    labels: list[str] = []
    for value in range(1, number + 1):
        order = str(value).zfill(2)
        labels.append(f"har{order}{voltage}{mode} [V]")

    return labels
