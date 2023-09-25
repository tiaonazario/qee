import sys
from typing import Literal
from PySide6.QtWidgets import QApplication, QMainWindow

from gui.app import CentralWidget
from gui.utils import QSS, Settings


class MainWindow(QMainWindow):
    """Cria a janela principal"""

    def __init__(self) -> None:
        super().__init__()

        self.qss = QSS("gui/styles/global.qss", self)
        self.settings = Settings()

        self.setWindowTitle("QEE")
        self.setMinimumSize(1000, 563)

        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)

        self.central_widget.title_bar_page.theme_button.set_icon(
            self.theme_icon(), (24, 24)
        )
        self.central_widget.title_bar_page.theme_button.clicked.connect(
            self.toggle_theme
        )

    def theme_icon(self) -> Literal["sun", "moon"]:
        """Seleciona o ícone"""
        if self.settings.values["theme"] == "light":
            return "sun"
        return "moon"

    def toggle_theme(self):
        """Altera o tema"""

        theme_name = self.settings.values["theme"]
        if theme_name == "light":
            self.settings.update({"theme": "dark"})
        else:
            self.settings.update({"theme": "light"})

        self.central_widget.title_bar_page.theme_button.set_icon(
            self.theme_icon(), (24, 24)
        )
        self.qss.apply()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
