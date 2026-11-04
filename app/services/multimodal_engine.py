# app/services/multimodal_engine.py
import base64
import logging
from langchain_core.messages import HumanMessage, SystemMessage
from app.core.config import settings
from app.core.image_service import codificar_imagen_base64
from app.core.llm_factory import get_llm

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Eres un asistente multimodal experto.
Analiza cuidadosamente las imágenes, audios y textos que recibas.
Responde de forma clara, concisa y en el idioma del usuario."""


class MultimodalEngine:
    def __init__(self):
        self.llm = get_llm()
        self.provider = settings.LLM_PROVIDER
        logger.info("🚀 MultimodalEngine listo (provider=%s)", self.provider)

    async def procesar(
        self,
        texto: str | None = None,
        imagen_bytes: bytes | None = None,
        audio_bytes: bytes | None = None,
        media_type_imagen: str = "image/jpeg",
        media_type_audio: str = "audio/mpeg",
    ) -> dict:
        contenido: list[dict] = []

        # 1. Audio → base64 (Nativo, sin Whisper externo)
        if audio_bytes:
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
            contenido.append({
                "type": "input_audio",  # Formato de OpenRouter/OpenAI para audio
                "input_audio": {
                    "data": audio_b64,
                    "format": _ext_from_mime(media_type_audio)
                }
            })

        # 2. Imagen → base64
        if imagen_bytes:
            imagen_b64 = codificar_imagen_base64(imagen_bytes)
            contenido.append({
                "type": "image_url",
                "image_url": {"url": f"data:{media_type_imagen};base64,{imagen_b64}"}
            })

        # 3. Texto del usuario
        if texto:
            contenido.append({"type": "text", "text": texto})

        if not contenido:
            raise ValueError("Debes enviar al menos texto, imagen o audio.")

        # 4. Invocar al LLM (OpenRouter procesará todo junto)
        mensajes = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=contenido),
        ]

        # Si hay audio, forzamos el uso del modelo de audio de OpenRouter
        current_llm = self.llm
        if audio_bytes and self.provider == "OPENROUTER":
            from langchain_openai import ChatOpenAI
            current_llm = ChatOpenAI(
                model=settings.OPENROUTER_AUDIO_MODEL,
                api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL,
                temperature=0,
            )

        respuesta = await current_llm.ainvoke(mensajes)

        usage = getattr(respuesta, "usage_metadata", {}) or {}
        return {
            "answer": respuesta.content,
            "tokens_used": {
                "prompt_tokens": usage.get("input_tokens", 0),
                "completion_tokens": usage.get("output_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
            "provider": self.provider,
        }


def _ext_from_mime(mime: str) -> str:
    """Mapea un MIME type a una extensión soportada por la API de audio."""
    return {
        "audio/mpeg": "mp3",
        "audio/wav": "wav",
        "audio/mp4": "m4a",
        "audio/ogg": "ogg",
    }.get(mime, "mp3")
