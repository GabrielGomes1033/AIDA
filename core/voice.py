import edge_tts
import uuid
from pathlib import Path

# Pasta onde os áudios gerados ficam salvos.
# mkdir(..., exist_ok=True) garante que a API não quebre se a pasta não existir.
AUDIO_DIR = Path("data/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Voz padrão do Edge TTS em português brasileiro.
DEFAULT_VOICE = "pt-BR-FranciscaNeural"


async def generate_voice_audio(
    text: str,
    voice: str = DEFAULT_VOICE
) -> str:
    """
    Gera áudio natural feminino em português brasileiro.
    Retorna o caminho do arquivo MP3.
    """

    # UUID evita colisão de nomes quando várias mensagens geram áudio.
    filename = f"aida_{uuid.uuid4().hex}.mp3"
    filepath = AUDIO_DIR / filename

    # edge_tts prepara a fala com voz, velocidade e volume definidos.
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate="+0%",
        volume="+0%"
    )

    # save é assíncrono porque a geração do áudio depende do serviço TTS.
    await communicate.save(str(filepath))

    return str(filepath)
