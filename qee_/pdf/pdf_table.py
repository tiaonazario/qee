from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle


class PDFTable:
    """Classe para criar tabela no PDF"""

    def __init__(self, headers: list[str], contents: list[list[str]]) -> None:
        self.headers = headers
        self.contents = contents
        self.data = [self.headers] + self.contents
        self.table = self.__build()

    def __build(self) -> Table:
        """Cria a tabela"""

        widths = []
        for col in self.headers:
            size = len(col) + 1
            widths.append(size * 10)

        table = Table(self.data, colWidths=widths)
        style = TableStyle(
            [
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#000000')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
                ('LINEBELOW', (0, -1), (-1, -1), 0.5, HexColor('#000000')),
                ('LINEBEFORE', (0, 0), (0, -1), 0.5, HexColor('#000000')),
                ('LINEAFTER', (-1, 0), (-1, -1), 0.5, HexColor('#000000')),
                ('LINEAFTER', (0, 0), (0, -1), 0.5, HexColor('#000000')),
                ('LINEAFTER', (0, 1), (1, -1), 0.5, HexColor('#000000')),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ]
        )
        table.setStyle(style)

        return table
