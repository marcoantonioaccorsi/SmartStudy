import os
import uuid
from pathlib import Path
import markdown

TEMP_EXPORT_DIR = Path("temp_exports")
TEMP_EXPORT_DIR.mkdir(exist_ok=True)
 
def export_summary(summary_text: str, format_type: str) -> str:
    """
    Gera um arquivo no formato escolhido (md, pdf, docx) a partir do texto do resumo.
    Retorna o caminho para o arquivo gerado.
    """
    if format_type == "md":
        return export_to_md(summary_text)
    elif format_type == "pdf":
        return export_to_pdf(summary_text)
    elif format_type == "docx":
        return export_to_docx(summary_text)
    else:
        raise ValueError("Formato inválido. Use 'md', 'pdf' ou 'docx'.")

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
    Exemplo usando pdfkit ou outra lib para gerar PDF.
    Aqui ilustramos pdfkit, mas você pode trocar por WeasyPrint ou outro.
    """
    unique_filename = f"{uuid.uuid4()}.pdf"
    pdf_path = TEMP_EXPORT_DIR / unique_filename

    # 1) Converter o summary_text (markdown ou HTML) para PDF
    # Exemplo, se 'pdfkit' e 'wkhtmltopdf' estiverem instalados:
    # pdfkit.from_string(summary_text, str(pdf_path))

    # Neste exemplo fictício, vamos apenas gerar um PDF vazio ou algo simples
    # pois pdfkit requer HTML. Uma opção é converter summary_text a HTML ou rodar
    # algo mais robusto. Faremos algo minimal:
    html_content = f"<html><body><pre>{summary_text}</pre></body></html>"
    # pdfkit.from_string(html_content, str(pdf_path))

    # Caso não queira depender de pdfkit, você poderia p.ex. usar ReportLab.
    # (aqui deixamos como pseudo-código)
    with open(pdf_path, "w", encoding="utf-8") as f:
        f.write("FAKE PDF - troque por pdfkit ou outra lib\n")
        f.write(summary_text)

    return str(pdf_path)

def export_to_docx(summary_text: str) -> str:
    """
    Cria um .docx usando python-docx.
    """
    unique_filename = f"{uuid.uuid4()}.docx"
    docx_path = TEMP_EXPORT_DIR / unique_filename

    # from docx import Document
    # doc = Document()
    # doc.add_paragraph(summary_text)
    # doc.save(docx_path)

    # Exemplo minimal:
    with open(docx_path, "w", encoding="utf-8") as f:
        f.write("FAKE DOCX - troque por python-docx e salve de verdade.\n")
        f.write(summary_text)

    return str(docx_path)
