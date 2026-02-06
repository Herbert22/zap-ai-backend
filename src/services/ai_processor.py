import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resposta_ia(mensagem_usuario: str, prompt_sistema: str = "Você é um assistente útil."):
    """
    Gera resposta inteligente usando GPT-4o.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Mais rápido e barato
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": mensagem_usuario}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro na IA: {str(e)}"
