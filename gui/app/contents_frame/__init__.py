import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QAbstractItemView,
    QScrollArea,
)

from gui.app.contents_frame.data_table_menu import DataTableMenu
from gui.app.contents_frame.result import Result
from gui.widgets import Table
from gui.layouts import HorizontalLayout, VerticalLayout
from qee.types import VoltageValueType


class ContentsFrame(QFrame):
    """Quadro com o conteúdo"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self._layout = HorizontalLayout(self)
        self._layout.setContentsMargins(16, 8, 16, 8)
        self._layout.setSpacing(8)

        self.data_area = QFrame(self)
        self._layout.addWidget(self.data_area)

        self.data_layout = VerticalLayout(self.data_area)
        self.data_layout.setSpacing(8)

        self.data_title = QLabel("Tabela de dados", self)
        self.data_title.setObjectName("data_title")
        self.data_title.setFixedHeight(25)
        self.data_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.data_layout.addWidget(self.data_title)

        self.data_table = Table(self)
        self.data_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectColumns
        )
        self.data_table.verticalHeader().setVisible(True)
        self.data_layout.addWidget(self.data_table)

        self.table_menu = DataTableMenu(self.data_table)

        self.analysis_frame = QFrame(self)
        self.analysis_frame.setFixedWidth(370)
        self.analysis_layout = VerticalLayout(self.analysis_frame)
        self.analysis_layout.setSpacing(8)
        self._layout.addWidget(self.analysis_frame)

        self.result_title = QLabel("Análises", self)
        self.result_title.setObjectName("result_title")
        self.result_title.setFixedSize(370, 25)
        self.result_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.analysis_layout.addWidget(self.result_title)

        self.result_area = QScrollArea(self.analysis_frame)
        self.result_frame = QFrame()
        self.result_area.setWidget(self.result_frame)
        self.analysis_layout.addWidget(self.result_area)
        self.result_area.setWidgetResizable(True)

        self.result_layout = VerticalLayout(self.result_frame)
        self.result_layout.setSpacing(8)
        self.result_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )

        self.result_items: list[Result] = []

    def remove_result(self, result: Result) -> None:
        """Remove o resultado"""
        self.result_layout.removeWidget(result)
        result.deleteLater()

        for item in self.result_items:
            if item == result:
                self.result_items.remove(item)

    def add_result(self, data_frame: pd.DataFrame, title: str):
        """Seta o resultado"""

        result = Result(self, data_frame)
        result.title.setText(title)
        self.result_layout.addWidget(result)

        result.remove_button.clicked.connect(
            lambda: self.remove_result(result)
        )

        self.result_items.append(result)
