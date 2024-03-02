from datetime import datetime

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class PDFTable:
    """Classe para criar tabela no PDF"""

    def __init__(self, headers: list[str], contents: list[list[str]]) -> None:
        self.headers = headers
        self.contents = contents
        self.data = [self.headers] + self.contents
        self.table = self.__build()

    def __build(self) -> Table:
        """Cria a tabela"""

        widths: list[int] = []
        for col in self.headers:
            size = len(col) + 1
            widths.append(size * 10)

        table = Table(self.data, colWidths=widths)
        style = TableStyle(
            [
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#343A40')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#F8F9FA')),
                ('LINEBELOW', (0, -1), (-1, -1), 0.5, HexColor('#ADB5BD')),
                ('LINEBEFORE', (0, 0), (0, -1), 0.5, HexColor('#ADB5BD')),
                ('LINEAFTER', (-1, 0), (-1, -1), 0.5, HexColor('#ADB5BD')),
                ('LINEAFTER', (0, 0), (0, -1), 0.5, HexColor('#ADB5BD')),
                ('LINEAFTER', (0, 1), (1, -1), 0.5, HexColor('#ADB5BD')),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ]
        )
        table.setStyle(style)

        return table


class PDF:
    """Classe para gerar PDF"""

    def __init__(self) -> None:
        self.elements: list[object] = []
        self.add_header()

    def add(self, element: object) -> None:
        """Adiciona um elemento ao PDF"""

        self.elements.append(element)

    def add_table(
        self, headers: list[str], contents: list[list[str]]
    ) -> Table:
        """Adiciona uma tabela ao PDF"""

        table = PDFTable(headers, contents).table
        self.elements.append(table)

        return table

    def add_spacer(self, width: int = 1, height: int = 12) -> None:
        """Adiciona um espaço ao PDF"""

        self.elements.append(Spacer(width, height))

    def add_text(self, text: str, style: ParagraphStyle | None = None) -> None:
        """Adiciona um texto ao PDF"""

        if style is None:
            style = ParagraphStyle(
                name='Normal',
                fontSize=12,
                spaceAfter=12,
            )

        self.elements.append(Paragraph(text, style))

    def add_subtitle(self, text: str):
        """Adiciona um título centralizado"""

        style = ParagraphStyle(
            name='Heading1',
            fontSize=10,
            alignment=1,
            spaceAfter=6,
        )

        self.elements.append(Paragraph(text, style))

    def add_header(self) -> None:
        """Adiciona um cabeçalho ao PDF"""

        style = ParagraphStyle(
            name='Heading1',
            fontName='Helvetica-Bold',
            fontSize=12,
            alignment=1,
            spaceAfter=6,
        )

        data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        elements = [
            Image('gui/assets/ufersa.png', width=23.3 * mm, height=36 * mm),
            Paragraph('UNIVERSIDADE FEDERAL RURAL DO SEMI-ÀRIDO', style),
            Paragraph('RELATÓRIO DE ANÁLISE DE QEE', style),
            Paragraph(f'Data do relatório: {data_atual}', style),
        ]
        self.elements += elements
        self.add_spacer(height=24)

    def add_title(
        self, title: str, style: ParagraphStyle | None = None
    ) -> None:
        """Adiciona um texto em negrito ao PDF"""

        if style is None:
            style = ParagraphStyle(
                name='Heading1',
                fontName='Helvetica-Bold',
                fontSize=12,
                spaceAfter=12,
            )

        self.elements.append(Paragraph(title, style))

    def build(
        self,
        filename: str,
        pagesize: tuple[float, float] = A4,
        margin: tuple[float, float, float, float] = (
            30 * mm,
            30 * mm,
            20 * mm,
            20 * mm,
        ),
    ) -> None:
        """Gera o PDF"""

        doc = SimpleDocTemplate(
            filename,
            pagesize=pagesize,
            leftMargin=margin[0],
            topMargin=margin[1],
            rightMargin=margin[2],
            bottomMargin=margin[3],
        )

        store = self.elements

        doc.build(store)
