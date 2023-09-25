import os
from typing import Optional, Literal
from PySide6.QtCore import QPoint, Qt, QRect, QEvent
from PySide6.QtGui import (
    QPainter,
    QPen,
    QBrush,
    QPixmap,
    QColor,
    QPaintEvent,
    QEnterEvent,
)
from PySide6.QtWidgets import QPushButton, QWidget, QLabel

from qee.gui import Settings


class IconButton(QPushButton):
    """Bottom com ícone"""

    def __init__(self, parent: QWidget, text: str) -> None:
        super().__init__(parent)

        self.settings = Settings()
        self.theme = self.settings.get_theme()

        self.icon_path = ""
        self.active = False
        self.text_ = text

        self.tooltip = Tooltip(self, text)
        self.tooltip.set_active(False)
        self.tooltip_position: Literal["left", "right"] = "left"

    def set_icon(self, icon: str) -> None:
        """Seta o ícone"""

        self.icon_path = icon
        self.repaint()

    def paint_icon(self, painter: QPainter, rect: QRect) -> None:
        """Desenha o ícone"""
        if self.icon_path == "":
            return

        app_path = os.path.abspath(os.getcwd())
        folder = "qee/gui/assets/icons/"
        path = os.path.join(app_path, folder)
        icon_path = os.path.normpath(os.path.join(path, self.icon_path))

        icon = QPixmap(icon_path)
        painter_ = QPainter(icon)
        painter_.setCompositionMode(QPainter.CompositionMode_SourceIn)

        if self.active:
            painter_.fillRect(icon.rect(), "")
        else:
            painter_.fillRect(icon.rect(), "")

        painter.drawPixmap(
            (rect.width() - icon.width()) / 2,
            (rect.height() - icon.height()) / 2,
            icon,
        )
        painter_.end()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Desenha o botão"""

        QPushButton.paintEvent(self, event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.NoPen)

        rect = QRect(0, 0, 40, self.height())

        if self.active:
            background = self.theme["hover"]["200"]
            color = self.theme["text"]["200"]

            brush = QBrush(QColor(self.theme["hover"]["300"]))
            selection_rect = QRect(0, 0, 2, self.height())
            painter.setBrush(brush)
            painter.drawRoundedRect(selection_rect, 0, 0)
        else:
            background = "transparent"
            color = self.theme["text"]["200"]

        style = self.styleSheet()
        style += f"QPushButton {{ background-color: {background}; color: {color}; }}"
        self.setStyleSheet(style)

        self.paint_icon(painter, rect)
        painter.end()

    def move_tooltip(self):
        """Move o tooltip"""

        global_position = self.mapToGlobal(QPoint(0, 0))
        position = self.parent().mapFromGlobal(global_position)

        pos_x = position.x() + self.width()
        pos_y = position.y() + ((self.height() - self.tooltip.height()) / 2)

        self.tooltip.move(pos_x, pos_y)

    def enterEvent(self, event: QEnterEvent) -> None:
        """Evento de entrada"""

        QPushButton.enterEvent(self, event)

        self.active = True
        self.move_tooltip()
        self.tooltip.set_active(True)
        self.repaint()

    def leaveEvent(self, event: QEvent) -> None:
        """Evento de saída"""

        QPushButton.leaveEvent(self, event)

        self.active = False
        self.move_tooltip()
        self.tooltip.set_active(False)
        self.repaint()


class Tooltip(QWidget):
    """Dica de ferramenta"""

    def __init__(self, parent: QWidget, text: str) -> None:
        super().__init__(parent)

        self.active = True
        self.label = QLabel(text, self)
        self.label.adjustSize()
        height = (30 - self.label.height()) / 2
        self.label.move(15, height)
        self.setMinimumHeight(32)
        self.adjustSize()

        self.background = ""
        self.border = ""
        self.color = ""

    def set_colors(self, color: str, background: str, border: str):
        """Seta as cores do tooltip"""

        self.background = background
        self.border = border
        self.color = color

        style = f"background-color: transparent; color: {self.color};"
        self.label.setStyleSheet(style)
        self.repaint()

    def set_active(self, active: bool) -> None:
        """Seta o estado do tooltip"""

        if active is False:
            self.hide()
        else:
            self.show()
        self.active = active

    def paintEvent(self, event) -> None:
        """Desenha o tooltip"""
        QWidget.paintEvent(self, event)

        painter = QPainter(self)
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setWidth(1)
        pen.setBrush(QBrush(self.border, Qt.SolidPattern))
        painter.setPen(pen)
        painter.setBrush(QBrush(self.background, Qt.SolidPattern))

        width = self.label.width() + 25

        painter.drawPolygon(
            [
                QPoint(5, 0),
                QPoint(5, 10),
                QPoint(0, 15),
                QPoint(5, 20),
                QPoint(5, 30),
                QPoint(width, 30),
                QPoint(width, 0),
                QPoint(5, 0),
            ]
        )

        painter.end()
