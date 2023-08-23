"""
Modulo NLT

Este modulo contem a definição da classe NLT (Quantidade/Número de Leituras de Tensão)

Este modulo pode ser utilizado para criar instancias da classe NL e realizar quantificação
de tensões adequadas, precárias e críticas.
"""


class NLT:
    """
    Classe para trabalhar com a quantidade de leituras de tensão
    """

    def __init__(self, nla: int = 0, nlp: int = 0, nlc: int = 0) -> None:
        self.nla: int = nla
        self.nlp: int = nlp
        self.nlc: int = nlc

    def __str__(self) -> str:
        return f'{{"nla": {self.nla}, "nlp": {self.nlp}, "nlc": {self.nlc}}}'
