from typing import List, Tuple
import pandas as pd
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QSizePolicy,
    QScrollArea,
)

from qee.analysis import Analysis, Graphic
from qee.enums import VoltageValue
from qee.gui.layouts import HorizontalLayout, VerticalLayout
from qee.gui.utils import read_qss
from qee.gui.pages.home.result import Result
from qee.gui.pages.home.select_bar import SelectBar
from qee.gui.pages.home.table_menu import TableMenu
from qee.gui.components import Table, Title, VoltageDialog


class HomePage(QWidget):
    """Cria a página inicial"""

    def __init__(self, parent: QStackedWidget) -> None:
        super().__init__(parent)

        # self.path_file = "..."
        self.path_file = "D:/www/github/qee/data.csv"
        self.data_frame = pd.DataFrame()
        self.analysis = Analysis(self.data_frame)
        self.reference_voltage = VoltageValue.V220

        self.setStyleSheet(read_qss("qee/gui/pages/home/styles.qss"))

        self.page_layout = VerticalLayout(self)
        self.page_layout.setContentsMargins(10, 10, 10, 10)

        self.title = QLabel("Página inicial")
        self.title.setFixedHeight(30)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_layout.addWidget(self.title)

        self.select_bar = SelectBar(self, self.path_file)
        self.select_bar.open_button.clicked.connect(self.open_button_clicked)
        self.select_bar.load_button.clicked.connect(self.load_button_clicked)
        self.page_layout.addWidget(self.select_bar)

        self.content_frame = QFrame(self)
        self.page_layout.addWidget(self.content_frame)
        self.content_layout = HorizontalLayout(self.content_frame)

        self.data_table_frame = QFrame(self.content_frame)
        self.data_table_layout = VerticalLayout(self.data_table_frame)
        self.data_table_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_layout.addWidget(self.data_table_frame)

        self.data_title = QLabel("Tabela de dados", self.data_table_frame)
        self.data_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.data_title.setFixedHeight(30)
        self.data_table_layout.addWidget(self.data_title)

        self.data_table = Table(self.data_table_frame)
        self.data_table.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.data_table_layout.addWidget(self.data_table)

        self.table_menu = TableMenu(self.data_table)
        self.table_menu.graphic_button.triggered.connect(self.generate_graph)
        self.table_menu.voltage_variation_button.triggered.connect(
            self.voltage_variation
        )
        self.table_menu.harmonics_button.triggered.connect(self.harmonics)
        self.table_menu.voltage_imbalance_button.triggered.connect(
            self.voltage_imbalance
        )
        self.table_menu.frequency_button.triggered.connect(
            self.frequency_variation
        )

        self.result_area = QScrollArea()
        self.result_frame = QFrame()
        self.result_layout = VerticalLayout(self.result_frame)
        self.result_area.setMinimumWidth(300)
        self.result_area.setMaximumWidth(400)
        self.result_area.hide()
        self.result_area.setWidget(self.result_frame)
        self.result_area.setWidgetResizable(True)

        self.result_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_layout.addWidget(self.result_area)

        self.result_items: list[Result] = []

    def show_menu(self, pos: tuple[int, int]) -> None:
        """Exibe o menu de contexto"""

        self.menu.exec(self.data_table.mapToGlobal(pos))

    def open_button_clicked(self) -> None:
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

        self.path_file = file_result[0]
        self.select_bar.path_edit.setText(file_result[0])

    def load_button_clicked(self) -> None:
        """Carrega os dados do arquivo em uma tabela"""

        self.data_frame = pd.read_csv(self.path_file, sep=";")
        self.data_table.load(self.data_frame)
        self.data_table.horizontalHeader().setDefaultSectionSize(120)
        self.analysis = Analysis(self.data_frame)

    def add_result(self, data: pd.DataFrame, title: str) -> None:
        """Seta o resultado"""
        result = Result(self.result_area, data)
        result.title.setText(title)
        self.result_layout.addWidget(result)
        self.result_area.setVisible(True)

        result.remove_button.clicked.connect(
            lambda: self.remove_result(result)
        )

        self.result_items.append(result)

    def remove_result(self, result: Result) -> None:
        """Remove o resultado"""

        self.result_layout.removeWidget(result)
        result.deleteLater()

        for item in self.result_items:
            if item == result:
                self.result_items.remove(item)

    def open_voltage_dialog(self) -> int:
        """Abre o diálogo de seleção de tensão"""

        dialog = VoltageDialog(self)
        response = dialog.exec()

        return response

    def selected_voltage(self, voltage: VoltageValue):
        """Seleciona a tensão"""

        self.reference_voltage = voltage

    def generate_graph(self) -> None:
        """Gera o gráfico"""

        response = self.open_voltage_dialog()

        if response == QDialog.DialogCode.Accepted:
            label = self.data_table.get_selected_columns()[0]
            x_axis: list[float] = list(range(1, 1009))
            y_axis: list[float] = self.data_frame[label].to_list()

            graphic = Graphic(x_axis, y_axis)
            graphic.voltage(self.reference_voltage)
            graphic.show()

    def voltage_variation(self) -> None:
        """Variação de tensão"""

        response = self.open_voltage_dialog()

        if response == QDialog.DialogCode.Accepted:
            labels = self.data_table.get_selected_columns()
            data = self.analysis.voltage_variation(
                labels, self.reference_voltage, False
            )

            self.add_result(data, "Variação de tensão")

    def harmonics(self) -> None:
        """Distorções harmonicas"""

        labels = self.data_table.get_selected_columns()
        data = self.analysis.harmonics(labels, False)

        self.add_result(data, "Distorções harmonicas")

    def voltage_imbalance(self) -> None:
        """Desequilíbrio de tensão"""

        labels = self.data_table.get_selected_columns()
        data = self.analysis.voltage_imbalance(labels, False)

        self.add_result(data, "Desequilíbrio de tensão")

    def frequency_variation(self) -> None:
        """Variação de frequência"""

        label = self.data_table.get_selected_columns()[0]
        data = self.analysis.frequency_variation(label, False)

        self.add_result(data, "Variação de frequência")
