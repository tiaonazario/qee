from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QWidget

from gui.layouts import HorizontalLayout
from gui.widgets import Button


class TitleBarPage(QWidget):
    """Barra de título da página"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.setFixedHeight(50)
        self._layout = HorizontalLayout(self)

        self.spacer = QFrame(self)
        self.spacer.setFixedWidth(50)
        self._layout.addWidget(self.spacer)

        self.title = QLabel('QEE - Qualidade de Energia Elétrica', self)
        self.title.setObjectName('title_page')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self.title)

        self.theme_button = Button(self)
        self.theme_button.setStatusTip('Alterar tema')
        self.theme_button.setObjectName('theme_button')
        self.theme_button.setFixedSize(50, 50)
        self._layout.addWidget(self.theme_button)
