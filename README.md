# SmartStudy

**SmartStudy** é um backend em **Python + FastAPI** que automatiza a geração de resumos a partir de vídeos (por exemplo, do YouTube ou vídeos locais).  
O fluxo principal envolve:

1. **Download** ou **extração** do áudio (via `yt-dlp` ou `FFmpeg`).  
2. **Transcrição** do áudio (usando [OpenAI Whisper](https://github.com/openai/whisper)).  
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
- **`yt-dlp`**  
- **`ffmpeg`**  
- **Chaves de API** para usar DeepSeek ou OpenAI GPT, caso queira resumir remotamente.  
- **Ollama** se for usar IA local (ex.: deepseek-r1:14b).

---

## Instalação e Execução

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/marcoantonioaccorsi/SmartStudy
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

4. **Rode o servidor**:
   ```bash
   uvicorn app.main:app --reload
   ```
   Abra [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver a **documentação Swagger**.

---

## Estrutura do Projeto

```
SMARSTUDY/
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
├── venv/
├── main.py
├── routers/
│   ├── local_ollama_router.py
│   ├── deepseek_router.py
│   ├── openai_router.py
│   ├── summary_router.py
│   ├── test_flow_router.py
│   ├── transcript_router.py
│   ├── video_router.py
│   └── __init__.py
├── services/
│   ├── local_ollama_service.py
│   ├── deepseek_service.py
│   ├── openai_service.py
│   ├── export_service.py
│   ├── test_audio_service.py
│   ├── transcript_service.py
│   ├── video_service.py
│   └── __init__.py
├── temp/
├── temp_audio/
├── temp_exports/
└── samples/
```

---

## **Principais Endpoints**

### **Videos**
- **`POST /videos/upload`**  
  *Upload de vídeo local.*  
  Envie um arquivo de vídeo para o servidor, que poderá extrair o áudio e processá-lo futuramente.

- **`POST /videos/download`**  
  *Download de vídeo (ou áudio) do YouTube.*  
  Recebe uma URL de YouTube e obtém o arquivo de áudio/vídeo localmente.

---

### **Convert to text**
- **`POST /text/transcribe`**  
  *Transcrever áudio em texto.*  
  Recebe o caminho de um arquivo de áudio (local) e retorna o texto transcrito (por exemplo, usando Whisper).

---

### **API DeepSeek**
- **`POST /deepseek/summary`**  
  *Gera resumo usando a API DeepSeek.*  
  Recebe um texto transcrito e um prompt, envia à API DeepSeek e retorna o resumo.

---

### **API OpenAI**
- **`POST /openai/summary`**  
  *Gera resumo usando OpenAI GPT (GPT-3.5, etc.).*  
  Recebe texto transcrito + prompt e retorna a resposta do modelo GPT.

---

### **Local Ollama DeepSeek**
- **`POST /ollama/summary`**  
  *Gera resumo localmente, via Ollama (deepseek-r1:14b).*  
  Executa um modelo local em sua máquina (chamando “ollama run”), processa o texto e retorna o resumo.

---

### **Export Summary**
- **`POST /export/summary/export`**  
  *Endpoint de exportação.*  
  Gera um arquivo (`.md`, `.pdf`, `.docx`) a partir de um texto de resumo e retorna-o para download.

---

### **Test Flow**
- **`POST /test-flow`**  
  *Executa todo o pipeline em um só endpoint.*  
  Faz download (YouTube) → transcreve → gera resumo → exporta, retornando o arquivo final para download. Útil para testes sem precisar chamar cada rota separadamente.

---

*(Use essas descrições no seu README ou documentação para orientar usuários sobre como consumir cada rota.)*

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

---

## Futuras Implementações

- **Autenticação e Multiusuário**: Permitir que cada usuário tenha histórico de transcrições e resumos.  
- **Armazenamento em DB**: Persistir textos, logs e configurações.  
- **Frontend em React**: Criar interface amigável para gerenciar uploads, downloads e resumos.  

---

Obrigado por conferir o **SmartStudy**!