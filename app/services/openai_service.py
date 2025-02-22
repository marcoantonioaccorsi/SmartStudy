import os
import requests

def get_openai_summary(raw_text: str, user_prompt: str) -> str:
    """
    Faz chamada à API do OpenAI GPT-3.5 e retorna um resumo (ou resposta) com base no prompt.

    Parâmetros:
    - raw_text: texto base (ex.: transcrição do vídeo)
    - user_prompt: instruções do usuário (ex.: "Resuma os tópicos principais")

    Retorna:
    - texto gerado pelo GPT (string)
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não está definida nas variáveis de ambiente.")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Exemplo de payload para GPT-3.5 (chat)
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Você é um assistente de resumo conciso para estudos."
            },
            {
                "role": "user",
                "content": f"{user_prompt}\n\nTexto: {raw_text}"
            }
        ],
        # Parâmetros opcionais:
        "temperature": 0.5,
        "max_tokens": 500
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()  # dispara exceção se 4xx/5xx

        data = response.json()
        # Normalmente, a resposta está em data["choices"][0]["message"]["content"]
        result_text = data["choices"][0]["message"]["content"]
        return result_text.strip()

    except requests.RequestException as e:
        raise RuntimeError(f"Erro HTTP ao chamar API OpenAI: {str(e)}")
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Formato inesperado da resposta do OpenAI: {str(e)}")
