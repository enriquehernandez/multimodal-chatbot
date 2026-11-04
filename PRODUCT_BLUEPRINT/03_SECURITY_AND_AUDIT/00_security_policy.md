# Security Policy

## 1. Manejo de Secretos
- Cero hardcoding de API keys.
- `.env` excluido en `.gitignore`.
- `.env.example` como plantilla.

## 2. Validación de Archivos
- Imágenes: validación con Pillow + límite de tamaño (`MAX_IMAGE_SIZE_MB`).
- Audio: validación de MIME type + límite de tamaño (`MAX_AUDIO_SIZE_MB`).
- Se rechazan archivos vacíos o corruptos con HTTP 400.

## 3. Privacidad
- Las imágenes y audios **no se persisten** en disco: se procesan en memoria.
- Solo se envían al proveedor del LLM los datos necesarios (base64 de la imagen, 
  transcripción del audio).
- No se loguean los bytes de los archivos, solo metadatos (tamaño, MIME type).

## 4. Prompt Injection
- El System Prompt instruye al LLM a responder solo sobre lo que ve/escucha.
- Se recomienda (futuro) añadir un nodo de "guardrails" con LangGraph.