def read_qss(filepath: str) -> str:
    """Ler um arquivo de estilo QSS"""

    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()
