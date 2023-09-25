import pandas as pd
from PySide6.QtWidgets import (
    QTableWidget,
    QWidget,
    QAbstractItemView,
    QTableWidgetItem,
)


class Table(QTableWidget):
    """Cria um componente de tabela"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.init()

    def set_size(self, width: int = 80, height: int = 30) -> None:
        """Define o tamanho da tabela"""

        rows = self.rowCount()
        columns = self.columnCount()

        self.setFixedWidth(width * columns + 2)
        self.setFixedHeight(height * (rows + 1))

    def init(self):
        """Inicializa a tabela"""

        self.verticalHeader().hide()
        self.verticalHeader().setStretchLastSection(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setDefaultSectionSize(80)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    def load(self, data_frame: pd.DataFrame) -> None:
        """Carrega os dados do DataFrame na tabela"""

        rows, columns = data_frame.shape

        header_labels = list(data_frame.columns)

        self.setRowCount(rows)
        self.setColumnCount(columns)
        self.setHorizontalHeaderLabels(header_labels)

        for row in range(rows):
            for column in range(columns):
                item = QTableWidgetItem(str(data_frame.iat[row, column]))
                self.setItem(row, column, item)

    def get_selected_columns(self) -> list[str]:
        """Retorna as colunas selecionadas"""

        selected_ranges = self.selectedRanges()
        columns_index: list[str] = []
        for selected_range in selected_ranges:
            left_column = selected_range.leftColumn()
            right_column = selected_range.rightColumn()

            columns_index.append(self.horizontalHeaderItem(left_column).text())

            if left_column != right_column:
                for column in range(left_column + 1, right_column + 1):
                    columns_index.append(
                        self.horizontalHeaderItem(column).text()
                    )

        return columns_index
