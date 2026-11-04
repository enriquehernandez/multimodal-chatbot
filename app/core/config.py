# app/core/config.py
from functools import lru_cache
from typing import Literal
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Solo dejamos los 3 proveedores
LLMProvider = Literal["OPENROUTER", "OPENAI", "GOOGLE"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    LLM_PROVIDER: LLMProvider = Field(default="OPENROUTER")

    # --- OpenRouter ---
    OPENROUTER_API_KEY: str | None = Field(default=None)
    OPENROUTER_MODEL: str = Field(default="google/gemini-2.5-flash")
    OPENROUTER_AUDIO_MODEL: str = Field(default="openai/gpt-4o-audio-preview")
    OPENROUTER_BASE_URL: str = Field(default="https://openrouter.ai/api/v1")

    # --- OpenAI ---
    OPENAI_API_KEY: str | None = Field(default=None)
    OPENAI_MODEL: str = Field(default="gpt-4o")

    # --- Google ---
    GOOGLE_API_KEY: str | None = Field(default=None)
    GOOGLE_MODEL: str = Field(default="gemini-1.5-pro")

    MAX_IMAGE_SIZE_MB: int = Field(default=10, ge=1, le=50)
    MAX_AUDIO_SIZE_MB: int = Field(default=25, ge=1, le=100)
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING",
                       "ERROR"] = Field(default="INFO")

    @field_validator("OPENROUTER_BASE_URL")
    @classmethod
    def _validate_https(cls, v: str) -> str:
        if not v.startswith("https://"):
            raise ValueError(f"La URL debe empezar con 'https://': {v}")
        return v

    def validate_provider_credentials(self) -> None:
        llm_required = {
            "OPENROUTER": [("OPENROUTER_API_KEY", self.OPENROUTER_API_KEY)],
            "OPENAI": [("OPENAI_API_KEY", self.OPENAI_API_KEY)],
            "GOOGLE": [("GOOGLE_API_KEY", self.GOOGLE_API_KEY)],
            # GROQ eliminado
        }
        missing = [name for name,
                   val in llm_required[self.LLM_PROVIDER] if not val]
        if missing:
            raise ValueError(
                f"Faltan credenciales: {', '.join(missing)}. Revisa tu .env")

    def get_active_llm_model(self) -> str:
        return {
            "OPENROUTER": self.OPENROUTER_MODEL,
            "OPENAI": self.OPENAI_MODEL,
            "GOOGLE": self.GOOGLE_MODEL,
            # GROQ eliminado
        }[self.LLM_PROVIDER]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
