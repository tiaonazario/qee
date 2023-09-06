from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor


class PDFTable:
    """Classe para criar tabela no PDF"""

    def __init__(self, header: list[str], rows: list[list[str]]) -> None:
        self.header = header
        self.rows = rows
        self.data = [self.header] + self.rows
        self.table = self.__build()

    def __build(self) -> Table:
        """Cria a tabela"""

        widths = []
        for col in self.header:
            size = len(col) + 1
            widths.append(size * 9)

        table = Table(self.data, colWidths=widths)
        style = TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#000000")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
                ("LINEBELOW", (0, -1), (-1, -1), 0.5, HexColor("#000000")),
                ("LINEBEFORE", (0, 0), (0, -1), 0.5, HexColor("#000000")),
                ("LINEAFTER", (-1, 0), (-1, -1), 0.5, HexColor("#000000")),
                ("LINEAFTER", (0, 0), (0, -1), 0.5, HexColor("#000000")),
                ("LINEAFTER", (0, 1), (1, -1), 0.5, HexColor("#000000")),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ]
        )
        table.setStyle(style)

        return table


class PDF:
    """Classe para gerar PDF"""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.elements = []

    def add(self, element: object) -> None:
        """Adiciona um elemento ao PDF"""

        self.elements.append(element)

    def create_table(self, header: list[str], rows: list[list[str]]) -> Table:
        """Adiciona uma tabela ao PDF"""

        return PDFTable(header, rows).table

    def add_spacer(self, width: int = 1, height: int = 12) -> None:
        """Adiciona um espaço ao PDF"""

        self.elements.append(Spacer(width, height))

    def add_text(self, text: str, style: ParagraphStyle | None = None) -> None:
        """Adiciona um texto ao PDF"""

        if style is None:
            style = ParagraphStyle(
                name="Normal",
                fontSize=12,
                spaceAfter=12,
            )

        self.elements.append(Paragraph(text, style))

    def add_subtitle(self, text: str):
        """Adiciona um título centralizado"""

        style = ParagraphStyle(
            name="Heading1",
            fontName="Helvetica-Bold",
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
                name="Heading1",
                fontName="Helvetica-Bold",
                fontSize=12,
                spaceAfter=12,
            )

        self.elements.append(Paragraph(title, style))

    def build(
        self,
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
            self.filename,
            pagesize=pagesize,
            leftMargin=margin[0],
            rightMargin=margin[1],
            topMargin=margin[2],
            bottomMargin=margin[3],
        )

        store = self.elements

        doc.build(store)


if __name__ == "__main__":
    TITLE = "Tensão V1"

    rows = [
        ["nla", "937", ""],
        ["nlp", "43", ""],
        ["nlc", "28", ""],
        ["DRP", "4,27%", "3%"],
        ["DRC", "2,78%", "0,5%"],
    ]

    header = ["Indicador", "Obtidos", "PRODIST"]

    pdf = PDF("qee.pdf")

    pdf.add_title(TITLE)
    pdf.add_subtitle("Tabela de Indicadores")

    table = pdf.create_table(header, rows)
    pdf.add(table)

    pdf.build()
