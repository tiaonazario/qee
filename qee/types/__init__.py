from typing import Literal

VoltageRangeType = Literal['cr-sup', 'ad-sup', 'ad-inf', 'cr-inf']
VoltageClassifyType = Literal['Adequada', 'Precária', 'Crítica']
FrequencyClassifyType = Literal['Adequada', 'Baixa', 'Alta']
PowerFactorClassifyType = Literal['Adequado', 'Crítico']
VoltageValueType = Literal[
    110, 120, 127, 208, 215, 220, 230, 240, 254, 380, 440
]
