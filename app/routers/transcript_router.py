from fastapi import APIRouter, HTTPException, Body
from pathlib import Path
from app.services.transcript_service import transcribe_audio_whisper

transcript_router = APIRouter()

@transcript_router.post("/transcribe")
def transcribe_audio(audio_path: str = Body(...)):
    """
    Recebe um caminho de arquivo de áudio
    e retorna o texto transcrito usando Whisper.
    """
    if not Path(audio_path).exists():
        raise HTTPException(status_code=400, detail="Arquivo de áudio não encontrado.")

    try:
        text = transcribe_audio_whisper(audio_path)
        return {"transcription": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
