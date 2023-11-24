from typing import Literal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QWidget


class Message(QMessageBox):
    """Cria uma caixa de mensagem"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        button = self.addButton("Ok", QMessageBox.ButtonRole.AcceptRole)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFixedSize(60, 30)

    def set_option(
        self, option: Literal["Informação", "Aviso", "Erro", "Pergunta"]
    ) -> None:
        """Seleciona as opções"""
        self.setWindowTitle(option)
        if option == "Aviso":
            self.setIcon(QMessageBox.Icon.Warning)
        elif option == "Erro":
            self.setIcon(QMessageBox.Icon.Critical)
        elif option == "Pergunta":
            self.setIcon(QMessageBox.Icon.Question)
        elif option == "Informação":
            self.setIcon(QMessageBox.Icon.Information)
