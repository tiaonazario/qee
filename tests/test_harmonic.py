# pyright: reportUnknownVariableType=none
# pyright: reportUnknownMemberType=none


import pandas as pd

from qee.classes import Harmonic
from qee.functions import harmonics_cols

FILE_NAME = './data/202304110900_202305011720_6_ET-5061C_harmonico.csv'
data_frame = pd.read_csv(FILE_NAME, sep=';')[harmonics_cols('V1')]
harmonic_values: list[float] = data_frame.loc[0].to_list()


def test_harmonic_dit_h() -> None:
    """
    Testa o calculo da distorção harmônica de tensão de ordem h
    """
    harmonic = Harmonic(harmonic_values[1:], harmonic_values[0])
    dit_h = harmonic.dit_h(219)

    assert dit_h


def test_harmonic_dtt() -> None:
    """
    Testa o calculo da distorção harmônica total de tensão
    """
    harmonic = Harmonic(harmonic_values[1:], harmonic_values[0])
    dtt = harmonic.dtt()

    assert dtt


def test_harmonic_dtt_p() -> None:
    """
    Testa o calculo da distorção harmônica total de tensão
    para as componentes pares não múltiplos de 3
    """
    harmonic = Harmonic(harmonic_values[1:], harmonic_values[0])
    dtt_p = harmonic.dtt_p()

    assert dtt_p


def test_harmonic_dtt_i() -> None:
    """
    Testa o calculo da distorção harmônica total de tensão
    para as componentes ímpares não múltiplos de 3
    """
    harmonic = Harmonic(harmonic_values[1:], harmonic_values[0])
    dtt_i = harmonic.dtt_i()

    assert dtt_i


def test_harmonic_dtt_3() -> None:
    """
    Testa o calculo da distorção harmônica total de tensão para as componentes múltiplas de 3
    """
    harmonic = Harmonic(harmonic_values[1:], harmonic_values[0])
    dtt_3 = harmonic.dtt_3()

    assert dtt_3
