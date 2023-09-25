import re
from PySide6.QtWidgets import QWidget


from gui.utils.settings import Settings
from gui.utils.theme import Theme


class QSS:
    """Aplica a folha de estilho QSS a um Widget"""

    def __init__(self, file: str, widget: QWidget) -> None:
        self.widget = widget
        self.file = file
        self.apply()

    def apply(self):
        """Aplica a folha de estilho QSS a um Widget"""

        with open(self.file, "r", encoding="utf-8") as qss_file:
            style = qss_file.read()

        settings = Settings()
        theme_name = settings.values["theme"]
        theme = Theme(theme_name).load()

        for color_type, colors in theme.items():
            for index, color in colors.items():
                style = re.sub(f"{color_type}-{index}", color, style)

        self.widget.setStyleSheet(style)
