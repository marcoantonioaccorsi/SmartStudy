import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do .env antes de qualquer uso

from fastapi import FastAPI
from app.routers.video_router import video_router
from app.routers.transcript_router import transcript_router
from app.routers.summary_router import summary_router
from app.routers.openai_router import openai_router
from app.routers.ollama_router import ollama_router
from app.routers.export_router import export_router
from app.routers.test_flow_router import test_flow_router

app = FastAPI()

# Inclui o router, definindo um prefixo "/videos" e tags
app.include_router(video_router, prefix="/videos", tags=["Videos"])
app.include_router(transcript_router, prefix="/convert", tags=["Convert to text"])
app.include_router(summary_router, prefix="/deepseek", tags=["API Deepseek"])
app.include_router(openai_router, prefix="/openai", tags=["API Openai"])
app.include_router(ollama_router, prefix="/ollama", tags=["Local Ollama Deepseek"])
app.include_router(export_router, prefix="/exportSummary", tags=["Export Summary"])
app.include_router(test_flow_router, prefix="/testFlow", tags=["Test Flow"])




@app.get("/")
def root():
    return {"message": "Teste ok!"}

