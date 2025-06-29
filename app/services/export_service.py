import os
import uuid
from pathlib import Path
import markdown
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap

TEMP_EXPORT_DIR = Path("temp_exports")
TEMP_EXPORT_DIR.mkdir(exist_ok=True)


def export_summary(summary_text: str, format_type: str) -> str:
    """
    Gera um arquivo no formato escolhido (md, pdf, docx) a partir do texto do resumo.
    Retorna o caminho para o arquivo gerado.
    """
    try:
        if format_type == "md":
            return export_to_md(summary_text)
        elif format_type == "pdf":
            return export_to_pdf(summary_text)
        elif format_type == "docx":
            return export_to_docx(summary_text)
        else:
            raise ValueError("Formato inválido. Use 'md', 'pdf' ou 'docx'.")
    except Exception as e:
        raise ValueError(f"Erro ao exportar resumo: {str(e)}")


def export_to_md(summary_text: str) -> str:
    """
    Cria um arquivo .md com o texto do resumo e retorna o caminho do arquivo.
    """
    unique_filename = f"{uuid.uuid4()}.md"
    md_path = TEMP_EXPORT_DIR / unique_filename

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(summary_text)

    return str(md_path)


def export_to_pdf(summary_text: str) -> str:
    """
    Gera um PDF real usando reportlab, com quebra automática de linha.
    """
    unique_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = TEMP_EXPORT_DIR / unique_filename

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    width, height = letter
    margin = 40
    max_width = width - 2 * margin
    font_name = "Helvetica"
    font_size = 12
    c.setFont(font_name, font_size)

    text_object = c.beginText(margin, height - margin)
    # Aproximação: quantos caracteres cabem em uma linha
    chars_per_line = int(max_width // (font_size * 0.6))

    for line in summary_text.split('\n'):
        wrapped_lines = textwrap.wrap(line, width=chars_per_line)
        for wrapped_line in wrapped_lines:
            text_object.textLine(wrapped_line)
    c.drawText(text_object)
    c.save()

    return str(pdf_path)


def export_to_docx(summary_text: str) -> str:
    """
    Cria um .docx real usando python-docx.
    """
    unique_filename = f"{uuid.uuid4()}.docx"
    docx_path = TEMP_EXPORT_DIR / unique_filename

    doc = Document()
    for line in summary_text.split('\n'):
        doc.add_paragraph(line)
    doc.save(str(docx_path))

    return str(docx_path)
