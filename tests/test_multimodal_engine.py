# tests/test_multimodal_engine.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from langchain_core.messages import AIMessage
from app.services.multimodal_engine import MultimodalEngine


@pytest.mark.asyncio
async def test_procesar_multimodal_completo(laptop_bsod_bytes, audio_soporte_bytes, monkeypatch):
    """Prueba el flujo completo con la nueva lógica de audio nativo."""

    # 1. Creamos la respuesta simulada
    mock_response = AIMessage(
        content="Veo en la imagen una pantalla azul y escucho a alguien preocupado.",
        usage_metadata={"input_tokens": 10,
                        "output_tokens": 5, "total_tokens": 15},
    )

    # 2. Creamos un mock para el LLM que se usará por defecto
    default_mock_llm = MagicMock()
    default_mock_llm.ainvoke = AsyncMock(return_value=mock_response)

    # 3. Parcheamos get_llm para el caso base
    monkeypatch.setattr(
        "app.services.multimodal_engine.get_llm", lambda: default_mock_llm)

    # 4. Parcheamos ChatOpenAI porque el motor lo instancia para el audio
    with patch("langchain_openai.ChatOpenAI") as MockChatOpenAI:
        audio_mock_llm = MagicMock()
        audio_mock_llm.ainvoke = AsyncMock(return_value=mock_response)
        MockChatOpenAI.return_value = audio_mock_llm

        engine = MultimodalEngine()

        resultado = await engine.procesar(
            texto="¿Qué ves y qué escuchas?",
            imagen_bytes=laptop_bsod_bytes,
            audio_bytes=audio_soporte_bytes,
        )

        assert "pantalla azul" in resultado["answer"].lower()
        assert resultado["tokens_used"]["total_tokens"] == 15

        # 5. Verificamos la estructura del mensaje
        # (Comprobamos que se llamó al mock de audio, no al default)
        audio_mock_llm.ainvoke.assert_called_once()
        mensajes = audio_mock_llm.ainvoke.call_args[0][0]
        human_message = mensajes[1]

        assert len(human_message.content) == 3
        assert human_message.content[0]["type"] == "input_audio"
        assert human_message.content[1]["type"] == "image_url"
        assert human_message.content[2]["type"] == "text"


@pytest.mark.asyncio
async def test_procesar_sin_contenido(monkeypatch):
    """Prueba que falle si no se envía nada."""
    local_mock_llm = MagicMock()
    monkeypatch.setattr(
        "app.services.multimodal_engine.get_llm", lambda: local_mock_llm)

    engine = MultimodalEngine()

    with pytest.raises(ValueError, match="Debes enviar al menos"):
        await engine.procesar()
