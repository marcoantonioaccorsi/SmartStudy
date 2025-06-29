import whisper
import os
import torch

# Modelos “tiny”, “base”, “medium” ou “large”.
model = whisper.load_model("tiny", device="cpu")


def transcribe_audio_whisper(audio_path: str) -> str:
    """
    Recebe o caminho de um arquivo de áudio e retorna o texto transcrito usando Whisper.
    """

    print(
        f"Dispositivo usado: {'CUDA' if torch.cuda.is_available() else 'CPU'}")

    result = model.transcribe(audio_path,
                              fp16=torch.cuda.is_available(),
                              language="pt",
                              task="transcribe"
                              )
    text = result["text"]

    if os.path.exists(audio_path):
        os.remove(audio_path)

    return text
