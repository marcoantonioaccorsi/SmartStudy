from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import Any
from app.services.video_service import (
    upload_video_to_local,
    download_youtube_video
)

video_router = APIRouter()

@video_router.post("/upload")
def upload_video(file: UploadFile = File(...)) -> Any:
    """
    Rota para upload de vídeo local.
    Retorna o caminho do arquivo salvo ou alguma identificação.
    """
    if not file:
        raise HTTPException(status_code=400, detail="Nenhum arquivo foi enviado.")

    saved_path = upload_video_to_local(file)
    return {"message": "Vídeo enviado com sucesso", "file_path": saved_path}


@video_router.post("/download")
def download_video(url: str = Form(...)) -> Any:
    """
    Rota para download de vídeo do YouTube via link.
    """
    if not url:
        raise HTTPException(status_code=400, detail="Nenhuma URL fornecida.")

    try:
        saved_path = download_youtube_video(url)
        return {"message": "Vídeo baixado com sucesso", "file_path": saved_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
