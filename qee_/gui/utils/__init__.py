import re
from typing import Literal
from PySide6.QtWidgets import QWidget

from qee.gui import Settings


def read_qss(filepath: str) -> str:
    """Ler um arquivo de estilo QSS"""

    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def qss(filepath: str, widget: QWidget) -> None:
    """Aplica um arquivo de estilo QSS"""

    qss_file = read_qss(filepath)

    settings = Settings()
    theme = settings.get_theme()

    for color_type, values in theme.items():
        for index, color in values.items():
            fetch_pattern = f"{color_type}-{index}"
            qss_file = re.sub(fetch_pattern, color, qss_file)

    widget.setStyleSheet(qss_file)
