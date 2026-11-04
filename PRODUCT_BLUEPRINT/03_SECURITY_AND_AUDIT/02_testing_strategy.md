# Estrategia de Testing

## 1. Unit Tests
- `test_config.py`: carga de variables de entorno.
- `test_llm_factory.py`: Registry Pattern (cada proveedor devuelve la instancia correcta, 
  proveedor inválido lanza ValueError).
- `test_image_service.py`: validación de imágenes (válida, corrupta, demasiado grande).
- `test_audio_service.py`: mock de AsyncOpenAI para no llamar a Whisper real.

## 2. Integration Tests
- `test_multimodal_engine.py`: mockea el LLM y los servicios, verifica que se construya 
  el mensaje multimodal correctamente (texto + imagen + transcripción).
- `test_main.py`: TestClient de FastAPI. Simula subida de archivos con `UploadFile`. 
  Verifica 200, 400 (sin contenido) y 500 (error interno).

## 3. Mocking Strategy
- **LLM:** mock de `BaseChatModel.ainvoke` devolviendo un `AIMessage` con `usage_metadata`.
- **Whisper:** mock de `AsyncOpenAI.audio.transcriptions.create`.
- **Imágenes:** se usan bytes de una imagen 1x1 PNG generada en `conftest.py`.
- **Audios:** se usan bytes dummy (no se transcriben realmente).

## 4. Cobertura
Objetivo: **100% en `app/`**, excluyendo `scripts/` (ingesta y evaluación).