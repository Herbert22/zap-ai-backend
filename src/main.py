from fastapi import FastAPI

app = FastAPI(title="Zap AI API")

@app.get("/")
def read_root():
    return {"message": "Zap AI Brain is Running 🧠"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
