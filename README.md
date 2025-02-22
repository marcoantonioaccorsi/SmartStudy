Abaixo segue um modelo de **README.md** mais enxuto e organizado, com **passo a passo** claro para rodar o projeto. Ajuste conforme seu estilo ou necessidades.

---

# SmartStudy

**SmartStudy** é um backend em **Python + FastAPI** que automatiza a geração de resumos a partir de vídeos (por exemplo, do YouTube).  
O fluxo principal envolve:

1. **Download** ou **extração** do áudio (via `yt-dlp` ou `FFmpeg`).  
2. **Transcrição** do áudio (usando [OpenAI Whisper](https://github.com/openai/whisper) ou outro STT).  
3. **Resumo** do texto transcrito, chamando IA (DeepSeek, OpenAI GPT, ou IA local via Ollama).  
4. **Exportação** do resumo em `.md`, `.pdf` ou `.docx`.  

> **Observação**: Este projeto **não** inclui autenticação/multiusuário nem salva dados em banco. É um MVP focado no **fluxo de transcrever e resumir**.

---

## Índice

1. [Pré-requisitos](#pré-requisitos)  
2. [Instalação e Execução](#instalação-e-execução)  
3. [Estrutura do Projeto](#estrutura-do-projeto)  
4. [Principais Endpoints](#principais-endpoints)  
5. [Fluxo Completo (Test Flow)](#fluxo-completo-test-flow)  
6. [Exportação de Resumos](#exportação-de-resumos)  
7. [Futuras Implementações](#futuras-implementações)  

---

## Pré-requisitos

- **Python 3.9+**  
- **`yt-dlp`** instalado (para download do YouTube) ou acessível via pip.  
- **`ffmpeg`** instalado (para extrair áudio, se necessário).  
- (Opcional) **Chaves de API** para usar DeepSeek ou OpenAI GPT, caso queira resumir remotamente.  
- (Opcional) **Ollama** se for usar IA local (ex.: deepseek-r1:14b).

---

## Instalação e Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/SmartStudy.git
   cd SmartStudy
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv venv
   # Linux/Mac
   source venv/bin/activate
   # Windows
   .\venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ou use `pip freeze > requirements.txt` caso ainda não tenha o arquivo.)*

4. **Rode o servidor**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Abra [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver a **documentação Swagger**.

---

## Estrutura do Projeto

```
SmartStudy/
├── app/
│   ├── main.py               # Ponto de entrada (FastAPI)
│   ├── routers/
│   │   ├── video_router.py
│   │   ├── transcript_router.py
│   │   ├── summary_router.py
│   │   └── test_flow_router.py   # Endpoint que faz tudo (download->transcrever->resumir->exportar)
│   ├── services/
│   │   ├── video_service.py      # Download de vídeo
│   │   ├── transcript_service.py # Transcrever áudio
│   │   ├── deepseek_service.py   # Resumo via DeepSeek
│   │   ├── openai_service.py     # Resumo via OpenAI GPT
│   │   ├── ollama_service.py     # Resumo local (ex. deepseek-r1:14b)
│   │   └── export_service.py     # Exportar resumo em .md, .pdf, .docx
│   └── __init__.py
├── .env            # Chaves de API (não versionar)
├── requirements.txt
└── README.md
```

---

## Principais Endpoints

- **`POST /videos/download`**: Recebe link do YouTube, pode retornar transcrição (dependendo da implementação).  
- **`POST /transcript/transcribe`**: Transcreve um arquivo de áudio (caminho local).  
- **`POST /summary/summary`**: Recebe texto transcrito + prompt, gera resumo via IA escolhida.  
- **`POST /files/export`**: Exporta o resumo em `.md`, `.pdf` ou `.docx`.  
- **`POST /test/test-flow`**: Endpoint “all-in-one” para testes (baixa do YouTube → transcreve → resume → exporta).

---

## Fluxo Completo (Test Flow)

Para **testar tudo** de uma vez, use **`POST /test/test-flow`** com JSON:

```json
{
  "youtube_url": "https://www.youtube.com/watch?v=XXXXXX",
  "user_prompt": "Resuma em tópicos",
  "summary_provider": "local",
  "export_format": "md"
}
```

1. Faz download do áudio (YouTube).  
2. Transcreve (Whisper).  
3. Gera resumo (IA local, GPT, ou DeepSeek).  
4. Exporta em `.md` e retorna o arquivo final para download.

---

## Exportação de Resumos

O **`export_service.py`** contém funções para gerar arquivos `.md`, `.pdf`, `.docx`.  
- **Markdown**: simplesmente salva o texto com extensão `.md`.  
- **PDF**: pode usar libs como `pdfkit` (requer `wkhtmltopdf`) ou `WeasyPrint`.  
- **DOCX**: usa `python-docx` para criar um documento Word.

O endpoint **`POST /files/export`** exemplifica como receber `{ "summary_text": "...", "format_type": "pdf" }` e devolver um arquivo via **FileResponse**.

---

## Futuras Implementações

- **Autenticação e Multiusuário**: Permitir que cada usuário tenha histórico de transcrições e resumos.  
- **Armazenamento em DB**: Persistir textos, logs e configurações.  
- **Frontend em React**: Criar interface amigável para gerenciar uploads, downloads e resumos.  
- **Orquestração Assíncrona**: Se for lidar com vídeos grandes, usar Celery/RQ para processar em segundo plano.

---

Feito! Se tiver dúvidas, abra uma [Issue](https://github.com/seu-usuario/SmartStudy/issues) ou entre em contato.  
Obrigado por conferir o **SmartStudy**!