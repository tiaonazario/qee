from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QStackedWidget,
    QWidget,
    QPushButton,
)

from qee.gui.layouts import VerticalLayout
from qee.gui import Settings


class SettingsPage(QWidget):
    """Cria a página de análise"""

    def __init__(self, parent: QStackedWidget) -> None:
        super().__init__(parent)

        self.settings = Settings()
        self.page_layout = VerticalLayout(self)

        self.title = QLabel("Configurações")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_layout.addWidget(self.title)

        self.content = QFrame(self)
        self.content_layout = VerticalLayout(self.content)
        self.page_layout.addWidget(self.content)

        self.button = QPushButton("Trocar tema", self.content)
        self.content_layout.addWidget(self.button)

        self.label = QLabel(self.content)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setText(f"Tema atual: {self.settings.values['theme']}")
        self.content_layout.addWidget(self.label)

        self.frame = QFrame(self)
        self.page_layout.addWidget(self.frame)
