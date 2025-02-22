import os
import uuid
import subprocess
from pathlib import Path

# Se precisar de configurações, você pode importar do config.py
# from app.config import SOME_CONFIG

TEMP_DIR = Path("temp")  # Pasta onde salvaremos os vídeos

# Garante que a pasta exista
TEMP_DIR.mkdir(exist_ok=True)

def upload_video_to_local(file_object) -> str:
    """
    Recebe o file_object (conteúdo do arquivo enviado pelo cliente),
    gera um nome de arquivo único, salva no TEMP_DIR.
    Retorna o caminho completo do arquivo salvo (string).
    """
    # Gera um nome único usando UUID
    unique_filename = f"{uuid.uuid4()}.mp4"
    save_path = TEMP_DIR / unique_filename

    # Salva o arquivo binário no disco
    with open(save_path, "wb") as f:
        f.write(file_object.read())

    return str(save_path)


def download_youtube_video(url: str) -> str:
    """
    Recebe uma URL do YouTube, chama yt-dlp via subprocess
    para baixar o vídeo no TEMP_DIR com um nome único.
    Retorna o caminho do arquivo salvo.
    """
    unique_filename = f"{uuid.uuid4()}.mp3"
    output_path = TEMP_DIR / unique_filename

    # Monta o comando de download usando yt-dlp
    # -o "{output_path}" define o nome do arquivo de saída
    # Nota: Por padrão, o yt-dlp gera nomes baseados em título do vídeo,
    # mas aqui forçamos um nome único.
    command = [
        "yt-dlp",
        "--no-playlist",
        "-x",                      # extrair apenas o áudio
        "--audio-format", "mp3",   # gerar um MP3
        "--audio-quality", "9",    # 9 = pior qualidade = menor arquivo
        url,
        "-o", str(output_path)     # nome do arquivo de saída
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        # Se der erro no download, podemos levantar exceção ou retornar algo
        raise RuntimeError(f"Erro ao baixar vídeo do YouTube: {e}")

    return str(output_path)
