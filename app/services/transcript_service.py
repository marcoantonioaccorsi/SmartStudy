import whisper

# Carrega o modelo do Whisper uma única vez (ex.: "small")
# Se você quiser usar GPU (CUDA), e tiver PyTorch com CUDA instalado:
# model = whisper.load_model("small", device="cuda")
# Podendo alterar para “tiny”, “base”, “medium” ou “large”.
model = whisper.load_model("small", device="cuda")

def transcribe_audio_whisper(audio_path: str) -> str:
    """
    Recebe o caminho de um arquivo de áudio e retorna o texto transcrito usando Whisper.
    """
    # Transcreve o áudio
    result = model.transcribe(audio_path)
    text = result["text"]
    return text


