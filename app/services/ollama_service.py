import subprocess
import re

def sanitize_ai_response(ai_text: str) -> str:
    """
    Remove trechos entre <think> e </think>, 
    além de possíveis espaços ou quebras extras.
    """
    # Remove tudo entre <think> e </think>
    clean_text = re.sub(r"<think>.*?</think>", "", ai_text, flags=re.DOTALL)
    return clean_text.strip()

def local_deepseek_summary(raw_text: str, user_prompt: str) -> str:
    """
    Chama o modelo 'deepseek-r1:14b' via Ollama em modo subprocess,
    enviando o prompt no parâmetro -p.

    Parâmetros:
    - raw_text: texto base (ex.: transcrição de um vídeo)
    - user_prompt: instruções (ex.: "Resuma em tópicos")

    Retorna:
    - Resposta do modelo local (string).
    """

    # 1. Montar o prompt (você pode formatar como preferir)
    prompt = (
        "System: Você é um assistente extremamente literal. "
        "Não invente fatos que não estejam no texto. "
        "Responda apenas com tópicos objetivos.\n\n"
        f"User: {user_prompt}\n\n"
        f"Texto: {raw_text}"
    )

    # 2. Comando a ser executado
    cmd = [
        "ollama", "run", "deepseek-r1:14b", prompt
        # Se quiser parâmetros extras (ex.: temperature), verifique se ollama run aceita:
        #"--temperature", "0"
    ]

    try:
        # 3. Executar via subprocess, capturando a saída
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,  # gera exceção se retornar código de erro
            encoding="utf-8" 
        )
        # 4. O stdout deve conter a resposta do modelo
        response_text = result.stdout.strip()
        clean_text = sanitize_ai_response(response_text)

        return clean_text

    except subprocess.CalledProcessError as e:
        # Se o comando retornar código != 0, cairemos aqui
        raise RuntimeError(f"Erro ao chamar ollama run: {e.stderr}")
 