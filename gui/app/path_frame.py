from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QFrame, QLineEdit

from gui.widgets import Button
from gui.layouts import HorizontalLayout


class PathFrame(QFrame):
    """Quadro de informação de caminho"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self._layout = HorizontalLayout(self)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.spacer_left = QFrame(self)
        self._layout.addWidget(self.spacer_left)

        self.central_frame = QFrame(self)
        self.central_frame.setObjectName("path_frame")
        self.central_frame.setFixedSize(560, 30)
        self._layout.addWidget(self.central_frame)

        self.central_layout = HorizontalLayout(self.central_frame)
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.central_layout.setSpacing(8)

        self.spacer_left = QFrame(self)
        self._layout.addWidget(self.spacer_left)

        self.label = QLabel("Arquivo: ", self.central_frame)
        self.label.setFixedWidth(60)
        self.central_layout.addWidget(self.label)

        self.path_edit = QLineEdit(self.central_frame)
        self.path_edit.setObjectName("path_edit")
        self.path_edit.setFixedSize(400, 25)
        self.central_layout.addWidget(self.path_edit)

        self.open_button = Button(self.central_frame)
        self.open_button.setFixedSize(30, 30)
        self.open_button.set_icon("folder-open")
        self.central_layout.addWidget(self.open_button)

        self.load_button = Button(self.central_frame)
        self.load_button.setFixedSize(30, 30)
        self.load_button.set_icon("loader")
        self.central_layout.addWidget(self.load_button)
