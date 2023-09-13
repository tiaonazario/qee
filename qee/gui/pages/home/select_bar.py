from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton

from qee.gui.layouts import HorizontalLayout


class SelectBar(QWidget):
    """Cria uma barra de seleção"""

    def __init__(self, parent: QWidget, path_file: str = "...") -> None:
        super().__init__(parent)

        self.setFixedHeight(30)
        self.layout_ = HorizontalLayout(self)
        self.layout_.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.label = QLabel("Tabela", self)
        self.label.setFixedWidth(60)
        self.layout_.addWidget(self.label)

        self.path_edit = QLineEdit(path_file, self)
        self.path_edit.setFixedWidth(400)
        self.layout_.addWidget(self.path_edit)

        self.open_button = QPushButton(self)
        self.open_button.setFixedSize(30, 30)
        self.open_button.setIcon(QIcon("assets/icons/folder-open.svg"))
        self.open_button.setIconSize(QSize(20, 20))
        self.layout_.addWidget(self.open_button)

        self.load_button = QPushButton(self)
        self.load_button.setFixedSize(30, 30)
        self.load_button.setIcon(QIcon("assets/icons/loader.svg"))
        self.load_button.setIconSize(QSize(20, 20))
        self.layout_.addWidget(self.load_button)
