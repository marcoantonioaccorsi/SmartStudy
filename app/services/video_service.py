import os
import uuid
import subprocess
from pathlib import Path

TEMP_DIR = Path("temp")

TEMP_DIR.mkdir(exist_ok=True)


def upload_video_to_local(file_object) -> str:
    """
    Recebe o arquivo, gera um nome de arquivo único, salva no TEMP_DIR.
    Retorna o caminho completo do arquivo salvo.
    """
    unique_filename = f"{uuid.uuid4()}.mp4"
    save_path = TEMP_DIR / unique_filename

    with open(save_path, "wb") as f:
        f.write(file_object.read())

    return str(save_path)


def download_youtube_video(url: str) -> str:
    """
    Recebe uma URL do YouTube, e baixa o vídeo no TEMP_DIR com um nome único.
    Retorna o caminho do arquivo salvo.
    """
    unique_filename = f"{uuid.uuid4()}.mp3"
    output_path = TEMP_DIR / unique_filename

    command = [
        "yt-dlp",
        "--no-playlist",
        "-x",                      # extrair apenas o áudio
        "--audio-format", "mp3",
        "--audio-quality", "9",    # 9 = pior qualidade = menor arquivo
        url,
        "-o", str(output_path)     # nome do arquivo de saída
    ]

    try:
        # Captura a saída para diagnóstico e depuração
        result = subprocess.run(command, check=True,
                                capture_output=True, text=True)

        # Verifica se o arquivo foi criado corretamente
        if not output_path.exists():
            # yt-dlp às vezes adiciona extensões
            base_name = unique_filename.split('.')[0]
            potential_files = list(TEMP_DIR.glob(f"{base_name}.*"))
            if potential_files:
                return str(potential_files[0])

        return str(output_path)
    except subprocess.CalledProcessError as e:
        error_detail = f"Saída: {e.stdout}\nErro: {e.stderr}" if hasattr(
            e, 'stdout') else str(e)
        raise RuntimeError(f"Erro ao baixar vídeo do YouTube: {error_detail}")
