from fastapi import FastAPI, Request
from src.services.audio_processor import processar_audio

app = FastAPI(title="Zap AI Brain")

@app.post("/webhook/wpp")
async def receive_webhook(request: Request):
    data = await request.json()
    
    # Verifica se é mensagem
    if "event" in data and data["event"] == "onMessage":
        msg = data.get("data", {})
        
        # Se for áudio (ptt = Push To Talk / Áudio gravado)
        if msg.get("type") == "ptt" or msg.get("type") == "audio":
            print("🎤 Áudio recebido! Processando...")
            # Pega URL (Nota: WPPConnect pode mandar base64 ou URL dependendo da config)
            # Vamos assumir que configuramos para mandar URL de download
            url = msg.get("mediaUrl") 
            if url:
                resultado = processar_audio(url)
                print(f"📝 Transcrição: {resultado}")
                return resultado
    
    return {"status": "ignored"}

@app.get("/")
def read_root():
    return {"message": "Zap AI Brain is Running 🧠"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
