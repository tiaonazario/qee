import pandas as pd
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QFrame, QLineEdit

from gui.widgets import Button, Table
from gui.layouts import HorizontalLayout, VerticalLayout


class Result(QWidget):
    """Componente contendo os indicadores obtidos"""

    def __init__(self, parent: QWidget, data_frame: pd.DataFrame) -> None:
        super().__init__(parent)

        self.data_frame = data_frame

        self._layout = VerticalLayout(self)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLineEdit(self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title.setObjectName("result_title_edit")
        self.title.setFixedHeight(20)
        self._layout.addWidget(self.title)

        self.frame = QFrame(self)
        self.frame_layout = HorizontalLayout(self.frame)
        self.frame_layout.setSpacing(8)
        self.frame_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._layout.addWidget(self.frame)

        self.table = Table(self.frame)
        self.table.load(data_frame)
        self.table.set_size()
        self.frame_layout.addWidget(self.table)

        self.buttons_frame = QFrame(self.frame)
        self.buttons_layout = VerticalLayout(self.buttons_frame)
        self.buttons_layout.setSpacing(8)
        self.buttons_frame.setFixedWidth(20)
        self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.frame_layout.addWidget(self.buttons_frame)

        self.remove_button = Button(self.buttons_frame)
        self.remove_button.setFixedSize(20, 20)
        self.remove_button.set_icon("x.svg")
        self.remove_button.setIconSize(QSize(15, 15))
        self.buttons_layout.addWidget(self.remove_button)

        self.save_button = Button(self.buttons_frame)
        self.save_button.setFixedSize(20, 20)
        self.save_button.set_icon("download.svg")
        self.save_button.setIconSize(QSize(15, 15))
        self.buttons_layout.addWidget(self.save_button)

        height = self.table.size().height() + self.title.size().height() + 20

        self.setFixedHeight(height)
