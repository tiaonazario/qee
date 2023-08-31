def get_file_extension(filename: str) -> str:
    """
    Pega a extensão de um arquivo.
    """
    parts = filename.split(".")

    if len(parts) > 1:
        return parts[-1]

    return ""
