import os
import requests
import ffmpeg
from openai import OpenAI

# Config OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def processar_audio(url_audio: str):
    """
    Baixa, converte e transcreve áudio do WhatsApp.
    """
    try:
        # 1. Baixar Arquivo
        response = requests.get(url_audio)
        if response.status_code != 200:
            return {"erro": "Falha ao baixar áudio"}
        
        filename = f"temp_{os.urandom(4).hex()}"
        ogg_path = f"/tmp/{filename}.ogg"
        mp3_path = f"/tmp/{filename}.mp3"
        
        with open(ogg_path, "wb") as f:
            f.write(response.content)
            
        # 2. Converter (OGG -> MP3) usando ffmpeg
        try:
            (
                ffmpeg
                .input(ogg_path)
                .output(mp3_path)
                .run(quiet=True, overwrite_output=True)
            )
        except ffmpeg.Error as e:
            return {"erro": f"Erro na conversão: {e}"}
            
        # 3. Transcrever (Whisper)
        with open(mp3_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
            
        # 4. Limpeza
        os.remove(ogg_path)
        os.remove(mp3_path)
        
        return {"texto": transcription.text}

    except Exception as ex:
        return {"erro": str(ex)}
