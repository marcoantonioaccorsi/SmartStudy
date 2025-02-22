# app/routers/ollama_router.py

from fastapi import APIRouter, HTTPException, Body
from app.services.ollama_service import local_deepseek_summary

ollama_router = APIRouter()

@ollama_router.post("/summary")
def generate_summary(
    transcribed_text: str = Body(...),
    user_prompt: str = Body(...)
):
    """
    Rota que chama o modelo local 'deepseek-r1:14b' via Ollama,
    passando o texto transcrito + prompt.
    """
    try:
        result = local_deepseek_summary(transcribed_text, user_prompt)
        return {"summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
