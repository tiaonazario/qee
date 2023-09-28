import json

from gui.types import ThemeType


class Theme:
    """Tema"""

    def __init__(self, name: str) -> None:
        self.name = name

    def load(self) -> ThemeType:
        """Carrega o terma"""

        path = 'gui/themes/' + self.name + '.json'

        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
