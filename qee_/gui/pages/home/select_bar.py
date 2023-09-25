from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit

from qee.gui.layouts import HorizontalLayout
from qee.gui.components import Button


class SelectBar(QWidget):
    """Cria uma barra de seleção"""

    def __init__(self, parent: QWidget, path_file: str = "...") -> None:
        super().__init__(parent)

        self.setFixedHeight(30)
        self.layout_ = HorizontalLayout(self)
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout_.setSpacing(8)

        self.label = QLabel("Arquivo", self)
        self.label.setFixedWidth(self.label.minimumSizeHint().width())
        self.layout_.addWidget(self.label)

        self.path_edit = QLineEdit(path_file, self)
        self.path_edit.setFixedHeight(30)
        self.path_edit.setFixedWidth(400)
        self.layout_.addWidget(self.path_edit)

        self.open_button = Button(self)
        self.open_button.setFixedSize(30, 30)
        self.open_button.set_icon("folder-open.svg")
        self.open_button.setIconSize(QSize(20, 20))
        self.layout_.addWidget(self.open_button)

        self.load_button = Button(self)
        self.load_button.setFixedSize(30, 30)
        self.load_button.set_icon("loader.svg")
        self.load_button.setIconSize(QSize(20, 20))
        self.layout_.addWidget(self.load_button)
