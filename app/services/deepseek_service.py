import os
import requests

def get_deepseek_summary(raw_text: str, user_prompt: str) -> str:
    """
    Envia o texto + prompt para a API do DeepSeek e retorna o resumo.

    Parâmetros:
    - raw_text: texto base (por exemplo, o texto transcrito de um vídeo)
    - user_prompt: instruções do usuário (ex: "Resuma os tópicos principais")

    Retorna:
    - resumo gerado pelo DeepSeek (string)
    """
    api_url = "https://api.deepseek.com/chat/completions" 

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY não está definida nas variáveis de ambiente.")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "Você é um especialista em resumos concisos para estudos."
            },
            {
                "role": "user",
                "content": f"{user_prompt}\n\nTexto: {raw_text}"
            }
        ],
        "model": "deepseek-chat",       # Ajustar o modelo
        "max_tokens": 2048,            
        "temperature": 0.5,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "response_format": {
            "type": "text"
        },
        "stop": None,
        "stream": False,
        "stream_options": None,
        "tools": None,
        "tool_choice": "none",
        "logprobs": False,
        "top_logprobs": None
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()  

        data = response.json()
        resumo = data["choices"][0]["message"]["content"]
        return resumo.strip()

    except requests.RequestException as e:
        raise RuntimeError(f"Erro HTTP ao chamar API DeepSeek: {str(e)}")
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Formato inesperado da resposta do DeepSeek: {str(e)}")
