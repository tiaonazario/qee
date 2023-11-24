from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QLabel,
    QPushButton,
    QFrame,
    QWidget,
    QRadioButton,
    QGroupBox,
    QCheckBox,
)

from gui.layouts import VerticalLayout, HorizontalLayout
from qee.constants import prodist


class VoltageDialog(QDialog):
    """Dialogo de seleção de valor de tensão"""

    def __init__(
        self,
        parent: QWidget,
        show_radios: bool = False,
        save_graphics: bool = False,
    ) -> None:
        super().__init__(parent)

        self.show_radios = show_radios
        self.save_graphics = save_graphics

        self.setWindowTitle("Níveis de tensões")
        self._layout = VerticalLayout(self)
        self._layout.setContentsMargins(16, 8, 16, 16)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._layout.setSpacing(8)

        self.title = QLabel("Selecione o nível de tensão")
        self.title.setObjectName("voltage_dialog_title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title.setFixedHeight(30)
        self._layout.addWidget(self.title)

        self.items = list(prodist.VOLTAGE_RANGE.keys())
        self.combo_box = QComboBox(self)
        self.combo_box.addItems([str(item) for item in self.items])
        self.combo_box.setFixedHeight(25)
        self.combo_box.setFixedWidth(100)
        self.combo_box.setCurrentText("220")
        self._layout.addWidget(
            self.combo_box, alignment=Qt.AlignmentFlag.AlignHCenter
        )

        self.check_graphics = QCheckBox("Salvar gráficos", self)
        self.check_graphics.setVisible(save_graphics)
        self._layout.addWidget(self.check_graphics)

        self.frame_groups = QFrame(self)
        self.frame_groups.setVisible(show_radios)
        self._layout.addWidget(self.frame_groups)
        self.frame_layout = HorizontalLayout(self.frame_groups)
        self.frame_layout.setSpacing(8)

        self.group_type = QGroupBox("Tipo:", self.frame_groups)
        self.frame_layout.addWidget(self.group_type)
        self.group_type_layout = VerticalLayout(self.group_type)

        self.check_phase_voltage = QRadioButton("Fase", self)
        self.check_phase_voltage.setChecked(True)
        self.group_type_layout.addWidget(self.check_phase_voltage)

        self.check_line_voltage = QRadioButton("Linha", self)
        self.group_type_layout.addWidget(self.check_line_voltage)

        self.group_values = QGroupBox("Valores:", self)
        self.frame_layout.addWidget(self.group_values)
        self.group_values_layout = VerticalLayout(self.group_values)

        self.check_avg_values = QRadioButton("Médios", self)
        self.check_avg_values.setChecked(True)
        self.group_values_layout.addWidget(self.check_avg_values)

        self.check_max_values = QRadioButton("Máximos", self)
        self.group_values_layout.addWidget(self.check_max_values)

        self.check_min_values = QRadioButton("Mínimos", self)
        self.group_values_layout.addWidget(self.check_min_values)

        self.choose_button = QPushButton("Selecionar")
        self.choose_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.choose_button.setObjectName("choose_button")
        self.choose_button.setFixedHeight(30)
        self.choose_button.clicked.connect(self.choose_option)
        self._layout.addWidget(self.choose_button)

    def check_options(self):
        """Seta as opções"""
        if self.check_phase_voltage.isChecked():
            self.parent().check_type = "fase"
        else:
            self.parent().check_type = "linha"

        if self.check_avg_values.isChecked():
            self.parent().check_values = "médios"
        elif self.check_max_values.isChecked():
            self.parent().check_values = "máximos"
        else:
            self.parent().check_values = "mínimos"

    def choose_option(self):
        """Retorna a opção selecionada"""

        value = int(self.combo_box.currentText())
        if value in self.items:
            self.parent().reference_voltage = value

            if self.show_radios:
                self.check_options()

            if self.save_graphics:
                self.parent().save_graphics = self.check_graphics.isChecked()

        self.accept()
