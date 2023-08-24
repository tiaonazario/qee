# pyright: reportUnknownVariableType=none
# pyright: reportUnknownMemberType=none

import pandas as pd
from pytest import raises

from qee.classes import Voltage
from qee.enums import ConsumerType, VoltageType, VoltageValue

VOLTAGE_FILE_NAME = './data/202304110900_202305011720_6_ET-5061C_tensao.csv'
data_frame = pd.read_csv(VOLTAGE_FILE_NAME, sep=';')

voltages_list: list[float] = data_frame['V1_Avg [V]'].head(1008).to_list()


def test_voltage_classify() -> None:
    """Testa a classificação de tensão"""

    voltage = Voltage()

    assert voltage.classify(220, VoltageValue.V220) == VoltageType.ADEQUATE
    assert voltage.classify(250, VoltageValue.V220) == VoltageType.CRITICAL
    assert voltage.classify(200, VoltageValue.V220) == VoltageType.PRECARIOUS


def test_voltage_reading_number_incorrectly_sized_voltages() -> None:
    """Testa se a quantidade de leituras possui o números de tensões corretas"""

    voltage = Voltage()
    error_message = 'Quantidade de leituras inválida, forneça 1008 valores de tensões lidas'

    with raises(ValueError) as error:
        voltage.reading_number([220, 250, 190], VoltageValue.V220)

    assert error.value.args[0] == error_message


def test_voltage_reading_number_correctly_sized_voltages() -> None:
    """Testa a quantidade de leituras"""

    voltage = Voltage()
    reading_number = voltage.reading_number(voltages_list, VoltageValue.V220)

    assert reading_number


def test_voltage_relative_duration_transgress() -> None:
    """Testa a duração relativa da transgressão"""

    voltage = Voltage()
    nlt = voltage.reading_number(voltages_list, VoltageValue.V220)
    drt = voltage.relative_duration_transgress(nlt.nlp, nlt.nlc)

    assert drt


def test_voltage_indicators() -> None:
    """Testa os indicadores de tensão"""

    voltage = Voltage()
    voltage_indicators = voltage.indicators(voltages_list, VoltageValue.V220)

    assert voltage_indicators


def test_voltage_compensation() -> None:
    """Testa a compensação de tensão"""

    voltage = Voltage()
    comp: float = voltage.compensation(4, 0.3, 1)
    comp_bt: float = voltage.compensation(6, 1, 1, ConsumerType.BT)
    comp_mt: float = voltage.compensation(6, 1, 1, ConsumerType.MT)
    comp_at: float = voltage.compensation(6, 1, 1, ConsumerType.AT)

    assert comp
    assert comp_bt
    assert comp_mt
    assert comp_at
