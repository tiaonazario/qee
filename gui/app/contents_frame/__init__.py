import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QScrollArea,
    QWidget,
    QPushButton,
)

from gui.app.contents_frame.data_table_menu import DataTableMenu
from gui.app.contents_frame.result import Result
from gui.layouts import HorizontalLayout, VerticalLayout
from gui.widgets import Button, Message, Table
from qee.classes import PDF
from qee.types import VoltageValueType


class ContentsFrame(QFrame):
    """Quadro com o conteúdo"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.message_box = Message(self)

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

        self.result_title_frame = QFrame(self.analysis_frame)
        self.result_title_frame.setFixedSize(370, 25)
        self.result_title_frame.setObjectName("result_title_frame")
        self.analysis_layout.addWidget(self.result_title_frame)

        self.result_title_layout = HorizontalLayout(self.result_title_frame)
        self.result_title_layout.setSpacing(8)

        self.result_title_spacer = QFrame(self.result_title_frame)
        self.result_title_spacer.setFixedWidth(20)
        self.result_title_layout.addWidget(self.result_title_spacer)

        self.result_title = QLineEdit("Análises", self.result_title_frame)
        self.result_title.setObjectName("result_title")
        self.result_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.result_title_layout.addWidget(self.result_title)

        self.save_button = Button(self.result_title_frame)
        self.save_button.set_icon("download.svg", (18, 18))
        self.save_button.setFixedSize(25, 25)
        self.save_button.clicked.connect(self.save_analysis)
        self.result_title_layout.addWidget(self.save_button)

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

    def get_save_file_name(self, filters: list[str]) -> tuple[str, str]:
        """Pegar o caminho do arquivo para salvar"""
        filter_join = ";;".join(filters)
        file_dialog = QFileDialog.getSaveFileName(
            self,
            "Salvar arquivo",
            "",
            filter=filter_join,
            selectedFilter=filters[0],
        )

        return str(file_dialog[0]), str(file_dialog[1])

    def remove_result(self, result: Result) -> None:
        """Remove o resultado"""
        self.result_layout.removeWidget(result)
        result.deleteLater()

        for item in self.result_items:
            if item == result:
                self.result_items.remove(item)

    def filename_not_selected(self) -> None:
        """Nenhum nome de arquivo foi selecionado"""
        self.message_box.setText("Nenhum nome de arquivo foi escolhido")
        self.message_box.set_option("Aviso")
        self.message_box.exec()

    def save_successful(self) -> None:
        """Sucesso ao salvar"""
        self.message_box.setText("Arquivo salvo com sucesso")
        self.message_box.set_option("Informação")
        self.message_box.exec()

    def save_result(self, data_frame: pd.DataFrame, title: str) -> None:
        """Salvar resultado"""
        filters = [
            "Formato CSV (*.csv)",
            "Formato PDF (*.pdf)",
            "Formato TXT (*.txt)",
            "Formato LaTex em TXT (*.txt)",
        ]
        path_file = self.get_save_file_name(filters)[0]
        filter_selected = self.get_save_file_name(filters)[1]
        if path_file == "":
            self.filename_not_selected()
            return

        if filter_selected == "Formato CSV (*.csv)":
            data_frame.to_csv(
                path_file, sep=";", index=False, encoding="utf-8"
            )
        elif filter_selected == "Formato PDF (*.pdf)":
            headers = data_frame.columns.tolist()
            contents: list[list[str]] = data_frame.values.tolist()

            pdf = PDF()
            pdf.add_subtitle(title)
            pdf.add_table(headers, contents)
            pdf.build(path_file)

        elif filter_selected == "Formato TXT (*.txt)":
            text = title + "\n" + data_frame.to_string()
            with open(path_file, "w", encoding="utf-8") as file:
                file.write(text)

        elif filter_selected == "Formato LaTex em TXT (*.txt)":
            latex = "Código LaTex\n"
            latex += data_frame.to_latex(index=False, escape=False) + "\n\n"
            with open(path_file, "w", encoding="utf-8") as file:
                file.write(latex)

        self.save_successful()

    def add_result(self, data_frame: pd.DataFrame, title: str) -> None:
        """Seta o resultado"""

        result = Result(self, data_frame)
        result.title.setText(title)
        self.result_layout.addWidget(result)

        result.remove_button.clicked.connect(
            lambda: self.remove_result(result)
        )

        text = result.title.text()
        result.save_button.clicked.connect(
            lambda: self.save_result(data_frame, text)
        )

        self.result_items.append(result)

    def save_analysis(self) -> None:
        """Salvar análise"""

        if len(self.result_items) == 0:
            self.message_box.set_option("Aviso")
            self.message_box.setText("Nenhum resultado foi adicionado")
            self.message_box.exec()
            return

        filters = [
            "Formato PDF (*.pdf)",
            "Formato TXT (*.txt)",
            "Formato LaTex em TXT (*.txt)",
        ]
        path_file = self.get_save_file_name(filters)[0]
        filter_selected = self.get_save_file_name(filters)[1]
        title = self.result_title.text()

        if path_file == "":
            self.filename_not_selected()
            return

        text = title + "\n"
        latex = "Código LaTex\n"
        for index, result in enumerate(self.result_items):
            data_frame = result.data_frame
            title_table = result.title.text()

            headers = data_frame.columns.tolist()
            contents: list[list[str]] = data_frame.values.tolist()
            if filter_selected == "Formato PDF (*.pdf)":
                if index == 0:
                    pdf = PDF()
                    pdf.add_title(title)

                pdf.add_spacer()
                pdf.add_subtitle(title_table)
                pdf.add_table(headers, contents)

                if index == len(self.result_items) - 1:
                    pdf.build(path_file)

            elif filter_selected == "Formato TXT (*.txt)":
                text += "\n" + title_table + "\n" + data_frame.to_string()

                if index == len(self.result_items) - 1:
                    with open(path_file, "w", encoding="utf-8") as file:
                        file.write(text)

            elif filter_selected == "Formato LaTex em TXT (*.txt)":
                latex += (
                    data_frame.to_latex(index=False, escape=False) + "\n\n"
                )
                with open(path_file, "w", encoding="utf-8") as file:
                    file.write(latex)

        self.save_successful()
