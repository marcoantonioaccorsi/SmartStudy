from fastapi import APIRouter, HTTPException, Body
from app.services.openai_service import get_openai_summary

openai_router = APIRouter()

@openai_router.post("/summary")
def generate_summary(
    transcribed_text: str = Body(...),
    user_prompt: str = Body(...)
):
    """
    Recebe texto transcrito + prompt e retorna um resumo via GPT-3.5.
    
    """
    try:
        resumo = get_openai_summary(transcribed_text, user_prompt)
        return {"summary": resumo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
