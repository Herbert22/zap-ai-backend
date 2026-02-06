import os
import requests

WPP_URL = os.getenv("WPP_URL", "http://wppconnect:3000")
WPP_SECRET = os.getenv("WPP_SECRET", "mysecrettoken")

def enviar_mensagem(session: str, phone: str, text: str):
    """
    Envia mensagem de texto via WPPConnect.
    """
    url = f"{WPP_URL}/api/{session}/send-message"
    
    payload = {
        "phone": phone,
        "message": text
    }
    
    headers = {
        "Authorization": f"Bearer {WPP_SECRET}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 201:
            print(f"✅ Mensagem enviada para {phone}")
            return True
        else:
            print(f"❌ Erro ao enviar: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão WPP: {e}")
        return False
