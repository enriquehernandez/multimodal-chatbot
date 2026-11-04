# app/main.py
import logging
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from app.core.config import settings
from app.models.schemas import ChatResponse, HealthResponse
from app.services.multimodal_engine import MultimodalEngine

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

try:
    settings.validate_provider_credentials()
except ValueError as e:
    logger.error("❌ Configuración inválida: %s", e)
    raise SystemExit(f"Configuración inválida: {e}")

app = FastAPI(
    title="Multimodal Chatbot API (Audio Nativo)",
    description="Chatbot con soporte de texto, imagen y audio usando OpenRouter.",
    version="0.2.0",
)
engine = MultimodalEngine()


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="ok",
        llm_provider=settings.LLM_PROVIDER,
        llm_model=settings.get_active_llm_model(),
        # stt_provider y stt_model ya no son necesarios
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(
    texto: str | None = Form(None),
    imagen: UploadFile | None = File(None),
    audio: UploadFile | None = File(None),
):
    imagen_bytes = await imagen.read() if imagen else None
    if imagen_bytes and len(imagen_bytes) > settings.MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            400, f"La imagen excede {settings.MAX_IMAGE_SIZE_MB} MB.")

    audio_bytes = await audio.read() if audio else None
    if audio_bytes and len(audio_bytes) > settings.MAX_AUDIO_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            400, f"El audio excede {settings.MAX_AUDIO_SIZE_MB} MB.")

    try:
        return await engine.procesar(
            texto=texto,
            imagen_bytes=imagen_bytes,
            audio_bytes=audio_bytes,
            media_type_imagen=imagen.content_type if imagen else "image/jpeg",
            media_type_audio=audio.content_type if audio else "audio/mpeg",
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.exception("Error interno")
        raise HTTPException(500, detail=f"Error interno: {e}")
