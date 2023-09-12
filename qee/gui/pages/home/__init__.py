import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from qee.analysis.graphic import Graphic
from qee.enums import VoltageValue
from qee.gui.layouts import HorizontalLayout, VerticalLayout
from qee.gui.utils import read_qss


class HomePage(QWidget):
    """Cria a página inicial"""

    def __init__(self, parent: QStackedWidget) -> None:
        super().__init__(parent)

        # self.path_file = "..."
        self.path_file = 'D:/www/github/qee/data.csv'
        self.data_frame = pd.DataFrame()

        self.setStyleSheet(read_qss('qee/gui/pages/home/styles.qss'))

        self.page_layout = VerticalLayout(self)

        self.title = QLabel('Página inicial')
        self.title.setFixedHeight(30)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_layout.addWidget(self.title)

        self.select_bar = QFrame(self)
        self.select_bar.setFixedHeight(20)
        self.select_bar_layout = HorizontalLayout(self.select_bar)
        self.page_layout.addWidget(self.select_bar)

        self.select_bar_label = QLabel('Dados', self.select_bar)
        self.select_bar_layout.addWidget(self.select_bar_label)

        self.select_bar_path = QLineEdit(self.path_file, self.select_bar)
        self.select_bar_path.setFixedWidth(400)
        self.select_bar_layout.addWidget(self.select_bar_path)

        self.open_button = QPushButton('Abrir', self.select_bar)
        self.open_button.clicked.connect(self.open_button_clicked)
        self.select_bar_layout.addWidget(self.open_button)

        self.load_button = QPushButton('Carregar', self.select_bar)
        self.load_button.clicked.connect(self.load_button_clicked)
        self.select_bar_layout.addWidget(self.load_button)

        self.table = QTableWidget(self)
        self.table.setMaximumWidth(600)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectColumns)
        self.page_layout.addWidget(self.table)

        self.menu = QMenu(self)
        self.generate_graph = self.menu.addAction('Gerar gráfico')
        self.generate_graph.triggered.connect(self.generate_graph_clicked)

        # Conectar um slot ao evento de clique do botão direito do mouse
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_menu)

        self.frame = QFrame(self)
        self.frame.setFixedHeight(50)
        self.page_layout.addWidget(self.frame)

    def show_menu(self, pos: tuple[int, int]) -> None:
        """Exibe o menu de contexto"""

        self.menu.exec(self.table.mapToGlobal(pos))

    def load_table(self, data_frame: pd.DataFrame) -> None:
        """Carrega os dados do DataFrame na tabela"""

        rows, columns = data_frame.shape

        self.table.setRowCount(rows)
        self.table.setColumnCount(columns)
        self.table.setHorizontalHeaderLabels(data_frame.columns)

        for row in range(rows):
            for column in range(columns):
                item = QTableWidgetItem(str(data_frame.iat[row, column]))
                self.table.setItem(row, column, item)

    def open_button_clicked(self) -> None:
        """Abre o gerenciador de arquivos"""

        filters = 'Arquivos CSV (*.csv);;Arquivos XLS (*.xls);;Arquivos XLSX (*.xlsx)'
        file_result = QFileDialog.getOpenFileName(
            self,
            'Abrir arquivo',
            '',
            filter=filters,
        )

        if file_result[0] == '':
            return

        self.path_file = file_result[0]
        self.select_bar_path.setText(file_result[0])

    def load_button_clicked(self) -> None:
        """Carrega os dados do arquivo em uma tabela"""

        self.data_frame = pd.read_csv(self.path_file, sep=';')
        self.load_table(self.data_frame)

    def get_selected_column(self) -> list[str]:
        """Retorna a coluna selecionada"""

        selected_ranges = self.table.selectedRanges()
        columns_index: list[str] = []
        for selected_range in selected_ranges:
            left_column = selected_range.leftColumn()
            right_column = selected_range.rightColumn()

            columns_index.append(
                self.table.horizontalHeaderItem(left_column).text()
            )

            if left_column != right_column:
                for column in range(left_column + 1, right_column + 1):
                    columns_index.append(
                        self.table.horizontalHeaderItem(column).text()
                    )

            # if left_column == right_column:
            #     return self.table.horizontalHeaderItem(left_column).text()

        return columns_index

    def generate_graph_clicked(self) -> None:
        """Gera o gráfico"""

        label = self.get_selected_column()[0]
        x_axis: list[float] = list(range(1, 1009))
        y_axis: list[float] = self.data_frame[label].to_list()

        graphic = Graphic(x_axis, y_axis)
        graphic.voltage(VoltageValue.V220)
        graphic.show()
