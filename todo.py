import sys
import pandas as pd
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QFrame,
    QScrollArea,
)


class TodoListApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Todo List App")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout_ = QVBoxLayout(self.central_widget)

        self.add_button = QPushButton("Adicionar Tarefa")
        self.layout_.addWidget(self.add_button)

        self.scroll_area = QScrollArea()
        self.todo_list_frame = QFrame()
        self.todo_list_layout = QVBoxLayout(self.todo_list_frame)
        self.scroll_area.setWidget(self.todo_list_frame)
        self.scroll_area.setWidgetResizable(True)
        self.layout_.addWidget(self.scroll_area)

        self.todo_items = []  # Lista para manter as tarefas

        self.add_button.clicked.connect(self.add_task)

        # Adicionar o botão "Salvar"
        self.save_button = QPushButton("Salvar")
        self.layout_.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_to_dataframe)

    def add_task(self):
        task_frame = QFrame()
        task_layout = QVBoxLayout(task_frame)

        task_label = QLabel("Tarefa:")
        task_line_edit = QLineEdit()
        remove_button = QPushButton("Remover")

        task_layout.addWidget(task_label)
        task_layout.addWidget(task_line_edit)
        task_layout.addWidget(remove_button)

        self.todo_list_layout.addWidget(task_frame)

        # Conectar o botão "Remover" à função de remoção
        remove_button.clicked.connect(lambda: self.remove_task(task_frame))

        # Adicionar a tarefa à lista
        self.todo_items.append(task_line_edit)

    def remove_task(self, task_frame):
        # Remove o item da lista de tarefas e libera a memória
        self.todo_list_layout.removeWidget(task_frame)
        task_frame.deleteLater()

        # Remove o QlineEdit associado da lista de tarefas
        for item in self.todo_items:
            if item.parent() == task_frame:
                self.todo_items.remove(item)

    def save_to_dataframe(self):
        # Crie um DataFrame com os itens da lista de tarefas
        data = [item.text() for item in self.todo_items]
        df = pd.DataFrame(data)
        print("\nLista de tarefas")
        print(df)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoListApp()
    window.show()

    # Execute o loop principal do aplicativo
    sys.exit(app.exec_())
