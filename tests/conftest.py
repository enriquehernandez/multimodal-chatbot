# tests/conftest.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from langchain_core.messages import AIMessage


@pytest.fixture
def laptop_bsod_bytes():
    with open("data/images/laptop_bsod.png", "rb") as f:
        return f.read()


@pytest.fixture
def audio_soporte_bytes():
    with open("data/audio/audio_soporte.mp3", "rb") as f:
        return f.read()


@pytest.fixture
def mock_llm_response():
    return AIMessage(
        content=(
            "Veo en la imagen que tu laptop sufrió un error crítico de Windows (pantalla azul). "
            "En el audio mencionas que tienes una entrega urgente."
        ),
        usage_metadata={"input_tokens": 1523,
                        "output_tokens": 65, "total_tokens": 1588},
    )


@pytest.fixture
def mock_llm(mock_llm_response):
    llm = MagicMock()
    llm.ainvoke = AsyncMock(return_value=mock_llm_response)
    return llm
