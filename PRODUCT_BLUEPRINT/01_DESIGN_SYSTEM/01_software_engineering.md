# Software Engineering

## Principios SOLID

### Single Responsibility Principle (SRP)
- `image_service.py`: Solo valida y codifica imágenes.
- `multimodal_engine.py`: Solo orquesta el flujo.
- `llm_factory.py`: Solo instancia los modelos de lenguaje.

### Open/Closed Principle (OCP)
Usamos el **Registry Pattern** en `llm_factory.py`. Si mañana queremos agregar Mistral, solo creamos `_build_mistral()` y lo agregamos al `_PROVIDER_REGISTRY`. El código central no se toca.

### Dependency Inversion Principle (DIP)
El `MultimodalEngine` depende de la abstracción `get_llm()`, no de `ChatOpenAI` o `ChatGoogle`.

## Testing Strategy
- **Mocks:** Usamos `AsyncMock` para simular las respuestas de OpenRouter y no gastar tokens.
- **Integration Tests:** `TestClient` de FastAPI simula peticiones multipart/form-data reales.
- **Coverage:** 100% en la carpeta `app/`, excluyendo scripts de evaluación.