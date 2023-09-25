from typing import Literal
import json

from gui.types import SettingsKeysType, ThemeNameType

SettingsUpdateType = (
    dict[Literal["name"], str]
    | dict[Literal["version"], str]
    | dict[Literal["description"], str]
    | dict[Literal["theme"], ThemeNameType]
    | dict[Literal["author"], str]
)


class Settings:
    """Configurações da aplicação"""

    def __init__(self) -> None:
        self.values = self.load()

    def load(self) -> dict[SettingsKeysType, str]:
        """Carrega as configurações do arquivo de configuração"""
        with open("settings.json", "r", encoding="utf-8") as file:
            return json.load(file)

    def update(self, setting: SettingsUpdateType) -> None:
        """Atualiza uma configuração"""
        key = list(setting.keys())[0]
        value = list(setting.values())[0]
        self.values[key] = value
        with open("settings.json", "w", encoding="utf-8") as file:
            json.dump(self.values, file, indent=4)
