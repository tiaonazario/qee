def harmonics_cols(voltage: str) -> list[str]:
    """Retorna uma lista com os nomes das colunas de acordo com uma tensão"""

    columns: list[str] = [
        "har01{voltage}_Avg [V]",
        "har02{voltage}_Avg [V]",
        "har03{voltage}_Avg [V]",
        "har04{voltage}_Avg [V]",
        "har05{voltage}_Avg [V]",
        "har06{voltage}_Avg [V]",
        "har07{voltage}_Avg [V]",
        "har08{voltage}_Avg [V]",
        "har09{voltage}_Avg [V]",
        "har10{voltage}_Avg [V]",
        "har11{voltage}_Avg [V]",
        "har12{voltage}_Avg [V]",
        "har13{voltage}_Avg [V]",
        "har14{voltage}_Avg [V]",
        "har15{voltage}_Avg [V]",
        "har16{voltage}_Avg [V]",
        "har17{voltage}_Avg [V]",
        "har18{voltage}_Avg [V]",
        "har19{voltage}_Avg [V]",
        "har20{voltage}_Avg [V]",
    ]

    for index, column in enumerate(columns):
        columns[index] = column.format(voltage=voltage)

    return columns
