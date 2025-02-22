# app/services/audio_service.py

import subprocess
import uuid
from pathlib import Path

TEMP_AUDIO_DIR = Path("temp_audio")
TEMP_AUDIO_DIR.mkdir(exist_ok=True)

def extract_audio_ffmpeg(video_path: str, output_format: str = "mp3") -> str:
    """
    Extrai o áudio de um arquivo de vídeo usando FFmpeg.
    :param video_path: caminho do arquivo de vídeo (ex.: "temp/xyz.mp4")
    :param output_format: formato do áudio de saída ("mp3", "wav", etc.)
    :return: caminho do arquivo de áudio gerado
    """
    if not Path(video_path).exists():
        raise FileNotFoundError(f"Arquivo de vídeo não encontrado: {video_path}")
    
    # Gera um nome de arquivo único
    unique_filename = f"{uuid.uuid4()}.{output_format}"
    audio_output_path = TEMP_AUDIO_DIR / unique_filename

    # Monta o comando FFmpeg para extrair o áudio
    # Exemplo (MP3): ffmpeg -i input.mp4 -vn -acodec libmp3lame output.mp3
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # desabilita video
        "-acodec", "libmp3lame" if output_format == "mp3" else "pcm_s16le",
        str(audio_output_path)
    ]

    # Executa o processo de conversão
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro ao extrair áudio: {e.stderr.decode('utf-8', errors='ignore')}")

    # Retorna o caminho do arquivo de áudio gerado
    return str(audio_output_path)
