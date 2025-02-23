import whisper
import os

# Modelos “tiny”, “base”, “medium” ou “large”.
model = whisper.load_model("small", device="cuda")

def transcribe_audio_whisper(audio_path: str) -> str:
    """
    Recebe o caminho de um arquivo de áudio e retorna o texto transcrito usando Whisper.
    """
    # Transcreve o áudio
    result = model.transcribe(audio_path)
    text = result["text"]

    if os.path.exists(audio_path):
        os.remove(audio_path)

    return text


