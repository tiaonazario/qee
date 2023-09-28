from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QDialog, QLabel, QPushButton, QWidget

from gui.layouts import VerticalLayout
from qee.constants import prodist


class VoltageDialog(QDialog):
    """Dialogo de seleção de valor de tensão"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.setWindowTitle('Níveis de tensões')
        self._layout = VerticalLayout(self)
        self._layout.setContentsMargins(16, 8, 16, 16)
        self._layout.setSpacing(8)

        self.title = QLabel('Selecione o nível de tensão')
        self.title.setObjectName('voltage_dialog_title')
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title.setFixedHeight(30)
        self._layout.addWidget(self.title)

        self.items = list(prodist.VOLTAGE_RANGE.keys())
        self.combo_box = QComboBox()
        self.combo_box.addItems([str(item) for item in self.items])
        self.combo_box.setFixedHeight(25)
        self.combo_box.setFixedWidth(100)
        self.combo_box.setCurrentText('220')
        self._layout.addWidget(self.combo_box)

        self.choose_button = QPushButton('Selecionar')
        self.choose_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.choose_button.setObjectName('choose_button')
        self.choose_button.setFixedHeight(30)
        self.choose_button.clicked.connect(self.choose_option)
        self._layout.addWidget(self.choose_button)

    def choose_option(self):
        """Retorna a opção selecionada"""

        value = int(self.combo_box.currentText())
        if value in self.items:
            self.parent().reference_voltage = value
        self.accept()
