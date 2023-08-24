from qee.classes.prodist import DRT, NLT, VoltageIndicators


def test_prodist_drt() -> None:
    """Testa a duração relativa de transgressão"""
    drt = DRT()

    assert str(drt)


def test_prodist_nlt() -> None:
    """Testa a quantidade de leituras de tensão"""
    nlt = NLT()

    assert str(nlt)


def test_prodist_voltage_indicators() -> None:
    """Testa a classe que trabalha com os indicadores de tensão"""
    nlt = NLT()
    drt = DRT()
    indicators = VoltageIndicators(nlt, drt)

    assert str(indicators)
