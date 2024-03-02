import json

from gui.types import SettingsKeysType, ThemeNameType


class Settings:
    """Configurações da aplicação"""

    def __init__(self) -> None:
        self.values: dict[SettingsKeysType, str] = self.load()

    def load(self) -> dict[SettingsKeysType, str]:
        """Carrega as configurações do arquivo de configuração"""
        with open('settings.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
        return config

    def update(self, key: SettingsKeysType, value: str) -> None:
        """Atualiza uma configuração"""
        self.values[key] = value
        with open('settings.json', 'w', encoding='utf-8') as file:
            json.dump(self.values, file, indent=4)

    def update_theme(self, theme: ThemeNameType) -> None:
        """Atualiza o tema"""
        self.update('theme', theme)
