# app/models/schemas.py
"""
Modelos Pydantic para request/response de la API multimodal.

Estos schemas definen el contrato público de la API y se usan para:
    - Validación automática de datos de entrada (FastAPI).
    - Documentación automática en Swagger (/docs).
    - Serialización de respuestas.

Nota: la entrada es `multipart/form-data` (por los archivos), por lo que
los campos de entrada se declaran directamente en el endpoint con `Form` y
`File`. Aquí solo modelamos la respuesta y los tipos internos reutilizables.
"""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


# ====== Enums ======
class MediaType(str, Enum):
    """Tipos MIME permitidos para imágenes y audios."""

    # Imágenes
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_WEBP = "image/webp"
    IMAGE_GIF = "image/gif"

    # Audios
    AUDIO_MP3 = "audio/mpeg"
    AUDIO_WAV = "audio/wav"
    AUDIO_M4A = "audio/mp4"
    AUDIO_OGG = "audio/ogg"


# ====== Modelos de respuesta ======
class TokenUsage(BaseModel):
    """Detalle de tokens consumidos por el LLM (para auditoría de costos)."""

    prompt_tokens: int = Field(
        default=0, ge=0, description="Tokens del prompt")
    completion_tokens: int = Field(
        default=0, ge=0, description="Tokens de la respuesta")
    total_tokens: int = Field(default=0, ge=0, description="Total de tokens")


class ChatResponse(BaseModel):
    """
    Respuesta del endpoint `/chat`.

    Attributes:
        answer: Texto de la respuesta generada por el LLM.
        tokens_used: Desglose de tokens consumidos.
        provider: Proveedor de LLM que generó la respuesta (útil para debug).
    """

    answer: str = Field(
        ...,
        description="Respuesta generada por el LLM multimodal",
        examples=[
            "En la imagen veo un coche rojo estacionado frente a un edificio."],
    )
    tokens_used: TokenUsage = Field(
        default_factory=TokenUsage,
        description="Tokens consumidos por el LLM",
    )
    provider: str = Field(
        default="unknown",
        description="Proveedor de LLM usado (OPENAI, AZURE_OPENAI, GROQ, GOOGLE)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "En la imagen se observa un coche rojo deportivo.",
                    "tokens_used": {
                        "prompt_tokens": 1523,
                        "completion_tokens": 28,
                        "total_tokens": 1551,
                    },
                    "provider": "OPENAI",
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Respuesta del endpoint `/health`."""
    status: Literal["ok"] = Field(
        default="ok", description="Estado del servicio")
    llm_provider: str = Field(description="Proveedor de LLM configurado")
    llm_model: str = Field(description="Modelo de LLM configurado")


class ErrorResponse(BaseModel):
    """Respuesta de error estándar de la API."""

    detail: str = Field(..., description="Mensaje de error legible")
    error_type: str | None = Field(
        default=None,
        description="Tipo de error (validation_error, internal_error, etc.)",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "detail": "La imagen excede el tamaño máximo permitido (10 MB).",
                    "error_type": "validation_error",
                }
            ]
        }
    }
