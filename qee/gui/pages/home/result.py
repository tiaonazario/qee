import pandas as pd
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QFrame, QPushButton

from qee.gui.components import Table, Title
from qee.gui.layouts import HorizontalLayout, VerticalLayout


class Result(QWidget):
    """Componente contendo os indicadores obtidos"""

    def __init__(self, parent: QWidget, data: pd.DataFrame) -> None:
        super().__init__(parent)

        self.data = data

        self.layout_ = HorizontalLayout(self)
        self.layout_.setSpacing(10)
        self.layout_.setContentsMargins(10, 10, 10, 10)
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.frame = QFrame(self)
        self.layout_.addWidget(self.frame)
        self.frame_layout = VerticalLayout(self.frame)
        self.frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = Title(self.frame)
        self.frame_layout.addWidget(self.title)

        self.table = Table(self.frame)
        self.table.load(data)
        self.table.set_size()
        self.frame_layout.addWidget(self.table)

        self.remove_button = QPushButton(self)
        self.remove_button.setFixedSize(20, 20)
        self.remove_button.setIcon(QIcon("assets/icons/x.svg"))
        self.remove_button.setIconSize(QSize(15, 15))
        self.layout_.addWidget(self.remove_button)

        width = (
            self.table.size().width() + self.remove_button.size().width() + 30
        )
        height = self.table.size().height() + self.title.size().height() + 20

        self.setFixedSize(width, height)
