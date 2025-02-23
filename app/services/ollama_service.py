import subprocess
import re

def sanitize_ai_response(ai_text: str) -> str:

    # Remove tudo entre <think> e </think>
    clean_text = re.sub(r"<think>.*?</think>", "", ai_text, flags=re.DOTALL)
    return clean_text.strip()

def local_deepseek_summary(raw_text: str, user_prompt: str) -> str:
    """
    Chama o modelo 'deepseek-r1:14b' via Ollama em modo subprocess.
    """
    prompt = (
        "System: Você é um assistente extremamente literal. "
        "Não invente fatos que não estejam no texto. "
        "Responda apenas com tópicos objetivos.\n\n"
        f"User: {user_prompt}\n\n"
        f"Texto: {raw_text}"
    )

    cmd = [
        "ollama", "run", "deepseek-r1:14b", prompt
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True, 
            encoding="utf-8" 
        )
        response_text = result.stdout.strip()
        clean_text = sanitize_ai_response(response_text)

        return clean_text

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Erro ao chamar ollama run: {e.stderr}")
 