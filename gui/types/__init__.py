from typing import Literal


ColorType = Literal["background", "border", "text", "table", "highlight"]
ColorIndexType = Literal["100", "200", "300"]
SettingsKeysType = Literal["name", "version", "description", "theme", "author"]
ThemeNameType = Literal["light", "dark"]

ThemeType = dict[ColorType, dict[ColorIndexType, str]]
