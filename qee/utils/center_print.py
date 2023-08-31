def center_print(text: str, size: int = 50) -> str:
    """Retorna um str com texto centralizado entre linhas"""

    line: str = "-" * size
    center: str = text.center(size, " ")

    return f"{line}\n{center}\n{line}"
