from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QMenu, QTableWidget


class DataTableMenu(QMenu):
    """Cria um menu de opções para a tabela"""

    def __init__(self, parent: QTableWidget) -> None:
        super().__init__(parent)

        self.table = parent

        self.graphic_button = self.addAction('Gerar gráfico')
        self.voltage_variation_button = self.addAction('Variação de tensão')
        self.power_factor_button = self.addAction('Fator de potência')
        self.harmonics_button = self.addAction('Distorções harmonicas')
        self.voltage_imbalance_button = self.addAction(
            'Desequilíbrio de tensão'
        )
        self.flicker_button = self.addAction('Flutuação de tensão')
        self.frequency_button = self.addAction('Variação de frequência')

        # Conectar um slot ao evento de clique do botão direito do mouse
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_menu)

    def show_menu(self, pos: QPoint) -> None:
        """Exibe o menu de contexto"""

        self.exec(self.table.mapToGlobal(pos))
