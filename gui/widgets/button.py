import os

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QWidget


class Button(QPushButton):
    """Botão"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_icon(self, icon: str, size: tuple[int, int] = (20, 20)) -> None:
        """Seta o ícone"""

        app_path = os.path.abspath(os.getcwd())
        folder = 'gui/assets/'
        path = os.path.join(app_path, folder)
        icon_path = os.path.normpath(os.path.join(path, icon))
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(size[0], size[1]))
