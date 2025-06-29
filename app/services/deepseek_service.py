import os
import requests
from dotenv import load_dotenv

def call_deepseek_api(payload: dict) -> dict:

    load_dotenv()

    api_url = "https://api.deepseek.com/chat/completions" 
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY não está definida no arquivo .env")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"  # Formato que funcionou no Postman
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)
        
        # Debug adicional
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        raise RuntimeError("Timeout na requisição para a API DeepSeek")
    except requests.RequestException as e:
        raise RuntimeError(f"Erro na requisição: {str(e)}")

def get_deepseek_summary(raw_text: str, user_prompt: str) -> str:
    """
    Versão ajustada do gerador de resumos
    """
    payload = {
        "model": "deepseek-chat",
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
        "stream": False 
    }

    try:
        data = call_deepseek_api(payload)
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Resposta inesperada da API: {str(e)}")