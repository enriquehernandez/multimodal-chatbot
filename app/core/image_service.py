# app/core/image_service.py
import base64
from PIL import Image
import io
from app.core.config import settings


def codificar_imagen_base64(imagen_bytes: bytes) -> str:
    """Valida y codifica una imagen en base64."""
    try:
        img = Image.open(io.BytesIO(imagen_bytes))
        img.verify()  # Lanza excepción si no es una imagen válida
    except Exception as e:
        raise ValueError(f"Imagen inválida: {e}")

    # Validar tamaño
    if len(imagen_bytes) > settings.MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise ValueError(
            f"La imagen excede {settings.MAX_IMAGE_SIZE_MB} MB"
        )
    return base64.b64encode(imagen_bytes).decode("utf-8")
