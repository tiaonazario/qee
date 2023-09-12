from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table

from qee.pdf.pdf_table import PDFTable


class PDF:
    """Classe para gerar PDF"""

    def __init__(self) -> None:
        self.elements: list[object] = []

    def add(self, element: object) -> None:
        """Adiciona um elemento ao PDF"""

        self.elements.append(element)

    def create_table(
        self, headers: list[str], contents: list[list[str]]
    ) -> Table:
        """Adiciona uma tabela ao PDF"""

        return PDFTable(headers, contents).table

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
            fontName='Helvetica-Bold',
            fontSize=10,
            alignment=1,
        )

        self.elements.append(Paragraph(text, style))

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
            20 * mm,
            20 * mm,
            20 * mm,
            20 * mm,
        ),
    ) -> None:
        """Gera o PDF"""

        doc = SimpleDocTemplate(
            filename,
            pagesize=pagesize,
            leftMargin=margin[0],
            rightMargin=margin[1],
            topMargin=margin[2],
            bottomMargin=margin[3],
        )

        store = self.elements

        doc.build(store)
