from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QWidget, QLabel, QComboBox, QPushButton

from qee.gui.layouts import VerticalLayout


from qee.enums import VoltageValue


class VoltageDialog(QDialog):
    """Dialogo de seleção de valor de tensão"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.setWindowTitle("Níveis de tensões")
        self.layout_ = VerticalLayout(self)
        self.layout_.setContentsMargins(30, 30, 30, 30)
        self.layout_.setSpacing(10)

        self.title = QLabel("Selecione o nível de tensão")
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title.setFixedHeight(30)
        self.layout_.addWidget(self.title)

        self.combo_box = QComboBox()
        self.combo_box.addItems([str(item.value) for item in VoltageValue])
        self.combo_box.setFixedHeight(25)
        self.combo_box.setFixedWidth(100)
        self.combo_box.setCurrentText("220")
        self.layout_.addWidget(self.combo_box)

        self.choose_button = QPushButton("Selecionar")
        self.choose_button.clicked.connect(self.choose_option)
        self.layout_.addWidget(self.choose_button)

    def choose_option(self):
        """Retorna a opção selecionada"""

        text = self.combo_box.currentText()

        self.parent().selected_voltage(VoltageValue[f"V{text}"])
        self.accept()
