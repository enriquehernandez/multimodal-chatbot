# tests/test_config.py
import pytest
from pydantic import ValidationError
from app.core.config import Settings


def test_default_values(monkeypatch):
    # Forzamos a que ignore el .env y use los defaults reales del código
    monkeypatch.setenv("LLM_PROVIDER", "OPENROUTER")
    # Si en config.py el default de OPENROUTER_MODEL es google/gemini-2.5-flash, esto pasará
    s = Settings(_env_file=None)

    assert s.LLM_PROVIDER == "OPENROUTER"
    # Asegúrate de que este sea el default en tu config.py
    assert s.get_active_llm_model() == "google/gemini-2.5-flash"


def test_missing_llm_credentials_raises():
    s = Settings(
        LLM_PROVIDER="OPENROUTER",
        OPENROUTER_API_KEY=None,
        _env_file=None  # Evita leer el .env local
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
