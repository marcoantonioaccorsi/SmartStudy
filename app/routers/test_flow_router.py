from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import FileResponse

from app.services.video_service import download_youtube_video
from app.services.transcript_service import transcribe_audio_whisper
from app.services.deepseek_service import get_deepseek_summary
from app.services.openai_service import get_openai_summary
from app.services.ollama_service import local_deepseek_summary
from app.services.export_service import export_summary

test_flow_router = APIRouter()

@test_flow_router.post("/test-flow")
def test_flow_endpoint(
    youtube_url: str = Body(...),
    user_prompt: str = Body(..., example="Resuma em tópicos principais."),
    summary_provider: str = Body(..., example="local"),  
    export_format: str = Body(..., example="md")   
):
    """
    Endpoint de teste que faz o fluxo completo (sem upload local):
    1) Baixa o vídeo do YouTube (áudio).
    2) Transcreve o áudio com Whisper.
    3) Gera resumo, usando o `user_prompt` e o `summary_provider` escolhido.
    4) Exporta o resumo no formato escolhido.
    5) Retorna o arquivo final para download.

    Exemplo de body JSON:
    {
      "youtube_url": "https://www.youtube.com/watch?v=XXXXXX",
      "user_prompt": "Crie um resumo bem objetivo",
      "summary_provider": "local",
      "export_format": "md"
    }
    """
    try:
        audio_path = download_youtube_video(youtube_url)

        transcribed_text = transcribe_audio_whisper(audio_path)

        if summary_provider == "local":
            summary_text = local_deepseek_summary(transcribed_text, user_prompt)
        elif summary_provider == "openai":
            summary_text = get_openai_summary(transcribed_text, user_prompt)
        elif summary_provider == "deepseek":
            summary_text = get_deepseek_summary(transcribed_text, user_prompt)
        else:
            raise HTTPException(status_code=400, detail="summary_provider inválido. Use 'local', 'openai' ou 'deepseek'.")

        export_path = export_summary(summary_text, export_format) 

        return FileResponse(
            export_path,
            media_type="application/octet-stream",
            filename=f"resumo.{export_format}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
