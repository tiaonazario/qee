import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QDialog,
    QLabel,
    QVBoxLayout,
    QWidget,
    QComboBox,
)


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dialog")

        self.comboBox = QComboBox()
        self.comboBox.addItems(["Opção 1", "Opção 2", "Opção 3"])

        self.ok_button = QPushButton("Escolher")
        self.ok_button.clicked.connect(self.choose_option)

        layout = QVBoxLayout()
        layout.addWidget(self.comboBox)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def choose_option(self):
        selected_option = self.comboBox.currentText()
        self.parent().update_option(selected_option)
        self.accept()


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 App")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.selected_option_label = QLabel("Opção Selecionada: ")

        self.open_dialog_button = QPushButton("Abrir Dialog")
        self.open_dialog_button.clicked.connect(self.open_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.selected_option_label)
        layout.addWidget(self.open_dialog_button)
        self.central_widget.setLayout(layout)

    def open_dialog(self):
        dialog = MyDialog(self)
        result = dialog.exec_()

    def update_option(self, selected_option):
        self.selected_option_label.setText(
            f"Opção Selecionada: {selected_option}"
        )


def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
