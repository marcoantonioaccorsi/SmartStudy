from fastapi import APIRouter, HTTPException, Body
from app.services.export_service import export_summary
from fastapi.responses import FileResponse

export_router = APIRouter()

@export_router.post("/export")
def export_endpoint(
    summary_text: str = Body(...),
    format_type: str = Body(...)
):
    """
    Recebe o texto do resumo e o formato desejado (md, pdf, docx).
    Gera o arquivo e retorna para download.
    Exemplo body:
    {
      "summary_text": "texto do resumo...",
      "format_type": "pdf"
    }
    """
    try:
        file_path = export_summary(summary_text, format_type)
        # Retornamos o arquivo. O FileResponse já lida com headers p/ download.
        return FileResponse(file_path, media_type="application/octet-stream", filename=f"resumo.{format_type}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
