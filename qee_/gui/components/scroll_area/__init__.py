from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QScrollArea, QWidget

from qee.gui.layouts import VerticalLayout


class ScrollArea(QScrollArea):
    """Componente que permite o uso de um scroll area"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.frame = QFrame()
        self.setMaximumWidth(370)
        self.layout_ = VerticalLayout(self.frame)
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setWidget(self.frame)
        self.setWidgetResizable(True)
