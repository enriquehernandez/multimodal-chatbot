# tests/test_config.py
import pytest
from pydantic import ValidationError
from app.core.config import Settings


def test_default_values():
    s = Settings()
    assert s.LLM_PROVIDER == "OPENROUTER"
    assert s.get_active_llm_model() == "nvidia/nemotron-3.5-super-vl:free"


def test_missing_llm_credentials_raises():
    s = Settings(
        LLM_PROVIDER="OPENROUTER",
        OPENROUTER_API_KEY=None,
    )
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        s.validate_provider_credentials()


def test_validate_provider_credentials_ok():
    s = Settings(
        LLM_PROVIDER="OPENROUTER",
        OPENROUTER_API_KEY="sk-or-test",
    )
    s.validate_provider_credentials()  # No debe lanzar


def test_validacion_url_invalida():
    with pytest.raises(ValidationError, match="La URL debe empezar con 'https://'"):
        Settings(OPENROUTER_BASE_URL="http://insecure-url.com")
