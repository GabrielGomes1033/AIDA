from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from core.aida import AIDA
from core.personality import get_intro
from core.voice import generate_voice_audio


# Instância principal da API FastAPI.
# É aqui que os endpoints HTTP da AIDA são registrados.
app = FastAPI(
    title="AIDA API",
    version="1.0.0",
    description="AIDA - Artificial Intelligence for Dialogue and Affection"
)

# Mantém uma única instância da AIDA enquanto o servidor estiver rodando.
# Isso permite reaproveitar o gerenciador de memória carregado no início.
aida = AIDA()


class ChatRequest(BaseModel):
    # Modelo do corpo enviado para POST /chat.
    # O FastAPI usa essa classe para validar os dados automaticamente.
    user_id: str = "default_user"
    message: str
    voice_enabled: bool = False


@app.get("/")
def home():
    # Endpoint simples de apresentação da API.
    # Útil para testar no navegador se o servidor está online.
    return {
        "name": "AIDA",
        "status": "online",
        "message": get_intro()
    }


@app.get("/health")
def health():
    # Endpoint de status com uma lista resumida das capacidades atuais.
    # Pode ser usado por uma interface ou monitoramento futuro.
    return {
        "status": "ok",
        "assistant": "AIDA",
        "features": [
            "interação humana",
            "memória seletiva",
            "continuidade de conversa",
            "opinião própria controlada",
            "detecção emocional simples",
            "respostas variadas por intenção",
            "voz feminina natural"
        ],
        "voice": {
            "enabled": True,
            "default_voice": "pt-BR-FranciscaNeural",
            "format": "mp3",
            "platforms": [
                "Android",
                "Windows",
                "iOS",
                "Linux",
                "Web"
            ]
        }
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    # Envia a mensagem para o motor principal da AIDA.
    # A resposta já inclui memória, histórico e intenção detectada.
    result = aida.chat(
        user_id=request.user_id,
        message=request.message
    )

    # Gera áudio somente quando o cliente pedir.
    # Isso evita gastar tempo criando MP3 em toda mensagem.
    if request.voice_enabled:
        audio_path = await generate_voice_audio(result["response"])
        result["audio_url"] = f"/audio/{audio_path.split('/')[-1]}"

    return result


@app.get("/audio/{filename}")
def get_audio(filename: str):
    # Entrega o arquivo MP3 gerado pela rota /chat quando voz está ativa.
    filepath = f"data/audio/{filename}"

    return FileResponse(
        filepath,
        media_type="audio/mpeg",
        filename=filename
    )
