# app/core/llm_factory.py
import logging
from typing import Callable
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq  <-- BORRAR
from app.core.config import settings

logger = logging.getLogger(__name__)


def _build_openrouter() -> BaseChatModel:
    logger.info("🔧 Construyendo LLM con OpenRouter (modelo: %s)",
                settings.OPENROUTER_MODEL)
    return ChatOpenAI(
        model=settings.OPENROUTER_MODEL,
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
        temperature=0,
        default_headers={
            "HTTP-Referer": "https://github.com/tu-usuario/multimodal-chatbot",
            "X-Title": "Multimodal Chatbot",
        },
    )


def _build_openai() -> BaseChatModel:
    logger.info("🔧 Construyendo LLM con OpenAI (modelo: %s)",
                settings.OPENAI_MODEL)
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=0,
    )


def _build_google() -> BaseChatModel:
    logger.info("🔧 Construyendo LLM con Google (modelo: %s)",
                settings.GOOGLE_MODEL)
    return ChatGoogleGenerativeAI(
        model=settings.GOOGLE_MODEL,
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0,
    )

# --- BORRAR _build_groq ---


_PROVIDER_REGISTRY: dict[str, Callable[[], BaseChatModel]] = {
    "OPENROUTER": _build_openrouter,
    "OPENAI": _build_openai,
    "GOOGLE": _build_google,
    # "GROQ": _build_groq,  <-- BORRAR
}


def get_llm() -> BaseChatModel:
    provider = settings.LLM_PROVIDER.upper()
    logger.info("🤖 [LLM FACTORY] Inicializando proveedor: %s", provider)

    builder = _PROVIDER_REGISTRY.get(provider)
    if not builder:
        raise ValueError(
            f"Proveedor no soportado: {provider}. "
            f"Usa uno de: {', '.join(_PROVIDER_REGISTRY.keys())}."
        )
    return builder()


def get_available_providers() -> list[str]:
    return list(_PROVIDER_REGISTRY.keys())
