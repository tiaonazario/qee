import json
from typing import Literal

ColorType = Literal["background", "text", "hover"]
ColorIndex = Literal["100", "200", "300", "400", "500"]
SettingsKeys = Literal["name", "version", "description", "theme", "author"]


class Settings:
    """Classe para armazenar as configurações do programa"""

    def __init__(self) -> None:
        self.values = self.load()
        self.theme_name = self.values["theme"]
        self.theme = self.get_theme()

    def load(self) -> dict[SettingsKeys, str]:
        """Carregar as configurações"""

        settings_path = "settings.json"
        with open(settings_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_theme(self) -> dict[ColorType, dict[ColorIndex, str]]:
        """Carregar o tema"""

        default_path = "qee/gui/themes/"
        theme_path = f"{default_path}{self.theme_name}.json"

        with open(theme_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def set_theme(
        self, theme_name: Literal["dark", "light", "default"]
    ) -> None:
        """Define o tema"""

        settings = self.values
        settings["theme"] = theme_name

        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4)
