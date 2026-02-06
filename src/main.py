from fastapi import FastAPI, Request
from src.services.audio_processor import processar_audio
from src.services.ai_processor import gerar_resposta_ia

app = FastAPI(title="Zap AI Brain")

@app.post("/webhook/wpp")
async def receive_webhook(request: Request):
    data = await request.json()
    
    # Verifica se é mensagem
    if "event" in data and data["event"] == "onMessage":
        msg = data.get("data", {})
        texto_entrada = ""
        
        # 1. Processar Entrada (Texto ou Áudio)
        if msg.get("type") == "chat":
            texto_entrada = msg.get("body", "")
            
        elif msg.get("type") == "ptt" or msg.get("type") == "audio":
            print("🎤 Áudio recebido! Processando...")
            url = msg.get("mediaUrl") 
            if url:
                transcricao = processar_audio(url)
                if "texto" in transcricao:
                    texto_entrada = transcricao["texto"]
                    print(f"📝 Transcrição: {texto_entrada}")
        
        # 2. Gerar Resposta (Se tiver texto válido)
        if texto_entrada:
            # TODO: Buscar prompt do cliente no banco
            prompt_teste = "Você é um assistente de advogado. Responda de forma curta e formal."
            resposta = gerar_resposta_ia(texto_entrada, prompt_teste)
            print(f"🤖 IA Respondeu: {resposta}")
            
            # TODO: Enviar resposta de volta pro WPPConnect
            return {"reply": resposta}
    
    return {"status": "ignored"}

@app.get("/")
def read_root():
    return {"message": "Zap AI Brain is Running 🧠"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
