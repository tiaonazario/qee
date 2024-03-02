from typing import Literal, TypedDict, get_type_hints

ColorType = Literal['background', 'border', 'text', 'table', 'highlight']
ColorIndexType = Literal['100', '200', '300']
SettingsKeysType = Literal['name', 'version', 'description', 'author', 'theme']
ThemeNameType = Literal['light', 'dark']

ThemeType = dict[ColorType, dict[ColorIndexType, str]]
