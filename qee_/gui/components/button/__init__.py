import os
from typing import Optional, Literal
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QWidget


class Button(QPushButton):
    """Botão"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.setCursor(Qt.PointingHandCursor)

    def set_icon(self, icon: str) -> None:
        """Seta o ícone"""

        app_path = os.path.abspath(os.getcwd())
        folder = "qee/gui/assets/icons/"
        path = os.path.join(app_path, folder)
        icon_path = os.path.normpath(os.path.join(path, icon))
        self.setIcon(QIcon(icon_path))
