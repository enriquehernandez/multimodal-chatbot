# tests/test_llm_factory.py
import pytest
from unittest.mock import patch
from app.core.llm_factory import get_llm, get_available_providers
from app.core.config import settings


def test_get_available_providers():
    providers = get_available_providers()
    assert "OPENROUTER" in providers
    assert "OPENAI" in providers
    assert "GOOGLE" in providers


@patch("app.core.llm_factory.ChatOpenAI")
def test_get_llm_openrouter(mock_chat_openai, monkeypatch):
    monkeypatch.setattr(settings, "LLM_PROVIDER", "OPENROUTER")
    monkeypatch.setattr(settings, "OPENROUTER_API_KEY", "sk-or-test")
    monkeypatch.setattr(settings, "OPENROUTER_MODEL",
                        "nvidia/nemotron-3.5-super-vl:free")

    get_llm()
    mock_chat_openai.assert_called_once()
    kwargs = mock_chat_openai.call_args.kwargs
    assert kwargs["model"] == "nvidia/nemotron-3.5-super-vl:free"
    assert kwargs["base_url"] == "https://openrouter.ai/api/v1"


def test_get_llm_invalid_provider(monkeypatch):
    monkeypatch.setattr(settings, "LLM_PROVIDER", "INVALID")
    with pytest.raises(ValueError, match="Proveedor no soportado"):
        get_llm()


def test_get_llm_openai(monkeypatch):
    monkeypatch.setattr(settings, "LLM_PROVIDER", "OPENAI")
    with patch("app.core.llm_factory.ChatOpenAI") as MockOpenAI:
        get_llm()
        MockOpenAI.assert_called_once()


def test_get_llm_google(monkeypatch):
    monkeypatch.setattr(settings, "LLM_PROVIDER", "GOOGLE")
    with patch("app.core.llm_factory.ChatGoogleGenerativeAI") as MockGoogle:
        get_llm()
        MockGoogle.assert_called_once()
