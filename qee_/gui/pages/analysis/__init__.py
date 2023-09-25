from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QStackedWidget, QWidget

from qee.gui.layouts import VerticalLayout


class AnalysisPage(QWidget):
    """Cria a página de análise"""

    def __init__(self, parent: QStackedWidget) -> None:
        super().__init__(parent)

        self.page_layout = VerticalLayout(self)

        self.title = QLabel("Analise de QEE")
        self.title.setFixedHeight(30)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_layout.addWidget(self.title)

        self.frame = QFrame(self)
        self.page_layout.addWidget(self.frame)
