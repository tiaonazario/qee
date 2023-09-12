from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton, QWidget


class IconButton(QPushButton):
    """Bottom com ícone"""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setIconSize(QSize(24, 24))
        self.icon_path = ''

    def set_icon(self, icon: str) -> None:
        self.icon_path = icon

        self.repaint()
