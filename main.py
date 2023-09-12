import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QWidget,
)

from qee.gui.layouts import HorizontalLayout, VerticalLayout
from qee.gui.pages import AnalysisPage, HomePage, SettingsPage


class MainWindow(QMainWindow):
    """Cria a janela principal"""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('QEE')
        self.setMinimumSize(960, 540)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget_layout = HorizontalLayout(self.central_widget)

        # BARRA LATERAL ESQUERDA
        self.sidebar = QWidget(self.central_widget)
        self.sidebar_layout = VerticalLayout(self.sidebar)
        self.central_widget_layout.addWidget(self.sidebar)

        self.home_button = QPushButton(self.sidebar)
        self.home_button.setFixedSize(50, 40)
        self.home_button.setIcon(QIcon('assets/icons/home.svg'))
        self.home_button.setIconSize(QSize(24, 24))
        self.home_button.clicked.connect(self.home_page_show)
        self.sidebar_layout.addWidget(self.home_button)

        self.analysis_button = QPushButton(self.sidebar)
        self.analysis_button.setFixedSize(50, 40)
        self.analysis_button.setIcon(QIcon('assets/icons/plug-zap.svg'))
        self.analysis_button.setIconSize(QSize(24, 24))
        self.analysis_button.clicked.connect(self.analysis_page_show)
        self.sidebar_layout.addWidget(self.analysis_button)

        self.spacer = QFrame(self.sidebar)
        self.sidebar_layout.addWidget(self.spacer)

        self.settings_button = QPushButton(self.sidebar)
        self.settings_button.setFixedSize(50, 40)
        self.settings_button.setIcon(QIcon('assets/icons/settings.svg'))
        self.settings_button.setIconSize(QSize(24, 24))
        self.settings_button.clicked.connect(self.settings_page_show)
        self.sidebar_layout.addWidget(self.settings_button)

        # PÁGINAS
        self.pages = QStackedWidget(self.central_widget)
        self.central_widget_layout.addWidget(self.pages)

        self.home_page = HomePage(self.pages)
        self.pages.addWidget(self.home_page)
        self.pages.setCurrentWidget(self.home_page)

        self.analysis_page = AnalysisPage(self.pages)
        self.pages.addWidget(self.analysis_page)

        self.settings_page = SettingsPage(self.pages)
        self.pages.addWidget(self.settings_page)

    def home_page_show(self) -> None:
        """Mostra a página inicial"""
        self.pages.setCurrentWidget(self.home_page)

    def analysis_page_show(self) -> None:
        """Mostra a página de análise de QEE"""
        self.pages.setCurrentWidget(self.analysis_page)

    def settings_page_show(self) -> None:
        """Mostra a página de configuração"""
        self.pages.setCurrentWidget(self.settings_page)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
