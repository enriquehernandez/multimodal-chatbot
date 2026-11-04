# tests/test_main.py
import importlib
from unittest.mock import patch, AsyncMock
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.services.multimodal_engine import MultimodalEngine

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "llm_provider" in data
    assert "llm_model" in data


def test_chat_multimodal_api(laptop_bsod_bytes, audio_soporte_bytes, monkeypatch):
    """Prueba el endpoint enviando imagen + audio, mockeando el procesamiento del motor."""

    # Creamos un mock asíncrono para el método procesar del motor
    fake_result = {
        "answer": "Veo una pantalla azul y escucho a alguien preocupado.",
        "tokens_used": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        "provider": "OPENROUTER"
    }
    mock_procesar = AsyncMock(return_value=fake_result)

    # Parcheamos la instancia del motor que ya está inicializada en main.py
    monkeypatch.setattr("app.main.engine.procesar", mock_procesar)

    files = {
        "imagen": ("laptop_bsod.png", laptop_bsod_bytes, "image/png"),
        "audio": ("audio_soporte.mp3", audio_soporte_bytes, "audio/mpeg"),
    }
    data = {"texto": "¿Qué problema tengo?"}

    response = client.post("/chat", data=data, files=files)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["answer"] == "Veo una pantalla azul y escucho a alguien preocupado."
    assert json_data["tokens_used"]["total_tokens"] == 15


def test_chat_sin_archivos():
    response = client.post("/chat")
    assert response.status_code == 400
    assert "Debes enviar al menos" in response.json()["detail"]


def test_validacion_credenciales_falla_al_arranque():
    with patch("app.core.config.Settings.validate_provider_credentials") as mock_validate:
        mock_validate.side_effect = ValueError("Error simulado")
        import app.main
        with pytest.raises(SystemExit, match="Configuración inválida"):
            importlib.reload(app.main)


def test_chat_imagen_demasiado_grande(monkeypatch):
    monkeypatch.setattr(settings, "MAX_IMAGE_SIZE_MB", 0)
    files = {"imagen": ("test.jpg", b"fake", "image/jpeg")}
    response = client.post("/chat", data={"texto": "test"}, files=files)
    assert response.status_code == 400
    assert "La imagen excede 0 MB" in response.json()["detail"]


def test_chat_audio_demasiado_grande(monkeypatch):
    monkeypatch.setattr(settings, "MAX_AUDIO_SIZE_MB", 0)
    files = {"audio": ("test.mp3", b"fake", "audio/mpeg")}
    response = client.post("/chat", data={"texto": "test"}, files=files)
    assert response.status_code == 400
    assert "El audio excede 0 MB" in response.json()["detail"]


def test_chat_error_interno_500(monkeypatch):
    async def mock_procesar_error(*args, **kwargs):
        raise Exception("Error simulado")

    monkeypatch.setattr("app.main.engine.procesar", mock_procesar_error)
    response = client.post("/chat", data={"texto": "test"})
    assert response.status_code == 500
    assert "Error interno" in response.json()["detail"]
