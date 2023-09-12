from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget


class VerticalLayout(QVBoxLayout):
    """Cria uma layout vertical"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class HorizontalLayout(QHBoxLayout):
    """Cria um layout horizontal"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
