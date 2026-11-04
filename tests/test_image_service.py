# tests/test_image_service.py
import pytest
from app.core.image_service import codificar_imagen_base64
from app.core.config import settings


def test_imagen_invalida():
    with pytest.raises(ValueError, match="Imagen inválida"):
        codificar_imagen_base64(b"esto no es una imagen")


def test_imagen_demasiado_grande(laptop_bsod_bytes, monkeypatch):
    # Forzamos un límite pequeño para que falle
    monkeypatch.setattr(settings, "MAX_IMAGE_SIZE_MB", 0.001)
    with pytest.raises(ValueError, match="excede"):
        codificar_imagen_base64(laptop_bsod_bytes)
