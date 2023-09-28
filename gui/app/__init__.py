import pandas as pd
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox, QWidget

from gui.app.contents_frame import ContentsFrame
from gui.app.path_frame import PathFrame
from gui.app.title_bar_page import TitleBarPage
from gui.app.voltage_dialog import VoltageDialog
from gui.layouts import VerticalLayout
from qee.classes import Analysis, Graphic
from qee.types import VoltageValueType


class CentralWidget(QWidget):
    """Widget Central da aplicação"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        path_file = "..."
        self.data_frame = pd.DataFrame()
        self.reference_voltage: VoltageValueType = 220
        self.analysis = Analysis(self.data_frame)

        self._layout = VerticalLayout(self)
        self.message_box = QMessageBox(self)
        button = self.message_box.addButton("Ok", QMessageBox.AcceptRole)
        button.setFixedSize(60, 30)

        self.title_bar_page = TitleBarPage(self)
        self._layout.addWidget(self.title_bar_page)

        self.path_frame = PathFrame(self)
        self.path_frame.path_edit.setText(path_file)
        self.path_frame.open_button.clicked.connect(self.open_file_dialog)
        self.path_frame.load_button.clicked.connect(self.load_button_clicked)
        self._layout.addWidget(self.path_frame)

        self.contents_frame = ContentsFrame(self)
        self._layout.addWidget(self.contents_frame)
        self.contents_frame.table_menu.graphic_button.triggered.connect(
            self.generate_graph
        )
        self.contents_frame.table_menu.voltage_variation_button.triggered.connect(
            self.voltage_variation
        )
        self.contents_frame.table_menu.power_factor_button.triggered.connect(
            self.power_factor
        )
        self.contents_frame.table_menu.harmonics_button.triggered.connect(
            self.harmonics
        )
        self.contents_frame.table_menu.voltage_imbalance_button.triggered.connect(
            self.voltage_imbalance
        )
        self.contents_frame.table_menu.frequency_button.triggered.connect(
            self.frequency_variation
        )

    def show_message(self, message: str) -> None:
        """Mostra uma mensagem na tela"""
        self.message_box.setWindowTitle("Erro")
        self.message_box.setIcon(QMessageBox.Icon.Critical)
        self.message_box.setText(message)
        self.message_box.exec()

    def open_file_dialog(self) -> None:
        """Abre o gerenciador de arquivos"""
        filters = "Arquivos CSV (*.csv);;Arquivos XLS (*.xls);;Arquivos XLSX (*.xlsx)"
        file_result = QFileDialog.getOpenFileName(
            self,
            "Abrir arquivo",
            "",
            filter=filters,
        )

        if file_result[0] == "":
            return

        self.path_frame.path_edit.setText(file_result[0])

    def load_button_clicked(self) -> None:
        """Carrega os dados do arquivo em uma tabela"""

        path_file = self.path_frame.path_edit.text()
        path_file_ext = path_file.rsplit(".", maxsplit=1)[-1]

        try:
            if path_file_ext == "csv":
                data_frame = pd.read_csv(path_file, sep=";")
            else:
                data_frame = pd.read_excel(path_file)
        except Exception:
            self.show_message("Forneça uma planilha válida")
            return

        if data_frame.shape[0] != 1008:
            self.show_message("A planilha deve conter 1008 linhas")
            return
        self.data_frame = data_frame

        self.contents_frame.data_table.load(self.data_frame)
        self.contents_frame.data_table.horizontalHeader().setDefaultSectionSize(
            120
        )

        self.analysis = Analysis(self.data_frame)

    def open_voltage_dialog(self) -> int:
        """Abre o diálogo de seleção de tensão"""
        dialog = VoltageDialog(self)
        return dialog.exec()

    def generate_graph(self) -> None:
        """Gera o gráfico"""

        response = self.open_voltage_dialog()
        if response == QDialog.DialogCode.Accepted:
            label = self.contents_frame.data_table.get_selected_columns()[0]

            x_axis: list[float] = list(range(1, 1009))
            y_axis: list[float] = self.data_frame[label].to_list()

            title = f"Gráfico com classificação de tensão ({label})"
            graphic = Graphic(x_axis, y_axis, title)
            graphic.voltage(self.reference_voltage)
            graphic.show()

    def voltage_variation(self) -> None:
        """Variação de tensão"""

        labels = self.contents_frame.data_table.get_selected_columns()
        if len(labels) != 3:
            self.show_message("Selecione três colunas referentes as tensões")
            return

        response = self.open_voltage_dialog()
        if response == QDialog.DialogCode.Accepted:
            data = self.analysis.voltage_variation(
                labels, self.reference_voltage
            )

            self.contents_frame.add_result(data, "Variação de tensão")

    def power_factor(self) -> None:
        """Fator de potência"""

        label = self.contents_frame.data_table.get_selected_columns()[0]
        data = self.analysis.power_factor(label)

        self.contents_frame.add_result(data, "Fator de potência")

    def harmonics(self) -> None:
        """Distorções harmonicas"""

        labels = self.contents_frame.data_table.get_selected_columns()
        data = self.analysis.harmonics(labels)

        self.contents_frame.add_result(data, "Distorções harmonicas")

    def voltage_imbalance(self) -> None:
        """Desequilíbrio de tensão"""

        labels = self.contents_frame.data_table.get_selected_columns()
        data = self.analysis.voltage_imbalance(labels)

        self.contents_frame.add_result(data, "Desequilíbrio de tensão")

    def frequency_variation(self) -> None:
        """Variação de frequência"""

        label = self.contents_frame.data_table.get_selected_columns()[0]
        data = self.analysis.frequency_variation(label)

        self.contents_frame.add_result(data, "Variação de frequência")
