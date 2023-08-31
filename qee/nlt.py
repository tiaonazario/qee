class NLT:
    """Classe para trabalhar com a quantidade de leituras de tensão"""

    def __init__(self, nla: int, nlp: int, nlc: int) -> None:
        self.nla = nla
        self.nlp = nlp
        self.nlc = nlc

    def to_dict(self) -> dict[str, int]:
        """Transforma a classe em um dicionário"""

        return {"nla": self.nla, "nlp": self.nlp, "nlc": self.nlc}

    def __str__(self) -> str:
        return str(self.to_dict())
