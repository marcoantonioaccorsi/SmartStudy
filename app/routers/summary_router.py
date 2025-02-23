from fastapi import APIRouter, HTTPException, Body
from app.services.deepseek_service import get_deepseek_summary

summary_router = APIRouter()

@summary_router.post("/summary")
def generate_summary(
    transcribed_text: str = Body(...),
    user_prompt: str = Body(...)
):
    """
    Recebe texto transcrito + prompt e retorna o resumo da API do DeepSeek.
    """
    try:
        resumo = get_deepseek_summary(transcribed_text, user_prompt)
        return {"summary": resumo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
