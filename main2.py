import sys

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QMainWindow,
    QStackedWidget,
    QWidget,
)

from qee.gui.layouts import HorizontalLayout, VerticalLayout
from qee.gui.pages import HomePage, SettingsPage
from qee.gui.utils import qss
from qee.gui import Settings
from qee.gui.components import Button


class MainWindow(QMainWindow):
    """Cria a janela principal"""

    def __init__(self) -> None:
        super().__init__()

        self.settings = Settings()

        qss("qee/gui/styles/global.qss", self)
        self.setWindowTitle("QEE")
        self.setMinimumSize(960, 540)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget_layout = HorizontalLayout(self.central_widget)

        # BARRA LATERAL ESQUERDA
        self.sidebar = QWidget(self.central_widget)
        self.sidebar.setObjectName("sidebar")
        self.sidebar_layout = VerticalLayout(self.sidebar)
        self.central_widget_layout.addWidget(self.sidebar)

        self.spacer = QFrame(self.sidebar)
        self.sidebar_layout.addWidget(self.spacer)

        self.settings_button = Button(self.sidebar)
        self.settings_button.setFixedSize(40, 40)
        self.settings_button.set_icon("settings.svg")
        self.settings_button.setIconSize(QSize(24, 24))
        self.settings_button.clicked.connect(self.settings_page_show)
        self.sidebar_layout.addWidget(self.settings_button)

        # PÁGINAS
        self.pages = QStackedWidget(self.central_widget)
        self.central_widget_layout.addWidget(self.pages)

        self.home_page = HomePage(self.pages)
        self.pages.addWidget(self.home_page)
        self.pages.setCurrentWidget(self.home_page)

        self.settings_page = SettingsPage(self.pages)
        self.settings_page.button.clicked.connect(self.toggle_theme)
        self.pages.addWidget(self.settings_page)

        self.current_page: QWidget = self.home_page

    def set_page(self, page: QWidget) -> None:
        """Define a página atual"""

        if self.current_page != page:
            self.current_page = page
        else:
            self.current_page = self.home_page

        self.pages.setCurrentWidget(self.current_page)

    def settings_page_show(self) -> None:
        """Mostra a página de configuração"""
        self.set_page(self.settings_page)

    def toggle_theme(self) -> None:
        """Trocar tema"""

        theme_name = self.settings.values["theme"]
        if theme_name == "dark":
            theme_name = "light"
            self.settings.set_theme(theme_name)
        else:
            theme_name = "dark"
            self.settings.set_theme(theme_name)
        self.settings_page.label.setText(f"Tema atual: {theme_name}")

        qss("qee/gui/styles/global.qss", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
