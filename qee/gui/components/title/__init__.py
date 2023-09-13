from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel


class Title(QLabel):
    """Componente de título"""

    def __init__(self, parent: QWidget, text: str = "") -> None:
        super().__init__(parent)

        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(self.minimumSizeHint().height())
