import os
import pytest
from app.services.audio_service import extract_audio_ffmpeg

TEST_VIDEO_PATH = "tests/samples/videoteste.mp4"

@pytest.mark.parametrize("output_format", ["mp3", "wav"])
def test_extract_audio_ffmpeg(output_format):
    """
    Verifica se a função extrai áudio de um vídeo sem erros
    e gera um arquivo não vazio.
    """
    # 1. Chama a função de extração
    audio_path = extract_audio_ffmpeg(TEST_VIDEO_PATH, output_format=output_format)

    # 2. Verifica se o arquivo foi criado
    assert os.path.exists(audio_path), f"Arquivo não encontrado: {audio_path}"

    # 3. Verifica se o arquivo não está vazio
    file_size = os.path.getsize(audio_path)
    assert file_size > 0, "Arquivo de áudio está vazio (0 bytes)"

    # 4. (Opcional) Apagar o arquivo após o teste
    #os.remove(audio_path)
