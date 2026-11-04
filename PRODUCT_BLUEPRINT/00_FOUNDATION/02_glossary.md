# Glosario Técnico de IA Multimodal

### ¿Qué es un LLM multimodal?
Un modelo que puede procesar más de un tipo de input (texto, imagen, audio) y 
razonar sobre ellos conjuntamente. Ej: GPT-4o, Gemini 1.5 Pro, Llama 3.2 Vision.

### ¿Qué es OpenRouter?
Es un enrutador de APIs que unifica el acceso a más de 100 modelos de lenguaje (LLMs) 
bajo una sola interfaz compatible con OpenAI. En este proyecto, lo usamos para 
procesar texto, imágenes y audio nativo con una sola API Key, permitiendo cambiar 
de modelo (ej. de Gemini a Nemotron) simplemente editando una variable de entorno.

### ¿Qué es Base64?
Codificación que convierte datos binarios (imágenes y audios) en texto ASCII. 
Los LLMs multimodales esperan los archivos en este formato dentro de un data URL: 
`data:image/jpeg;base64,<cadena>` o mediante bloques `input_audio`.

### ¿Qué es Pillow (PIL)?
Es la librería estándar de Python para el procesamiento de imágenes. En este 
proyecto se usa en `image_service.py` para **validar** que los archivos subidos 
por los usuarios sean imágenes reales y no archivos maliciosos camuflados 
(por ejemplo, un archivo ejecutable renombrado a `.jpg`).

### ¿Qué es Tool Calling?
Capacidad del LLM de invocar funciones externas (APIs, calculadoras, búsquedas). 
No lo usamos aún, pero LangGraph lo habilitaría en una próxima iteración.

### ¿Qué es LLM-as-a-Judge?
Técnica de evaluación donde un LLM "juez" califica la calidad de las respuestas 
de otro LLM. Lo usamos en `scripts/evaluate.py` para evitar Ragas (que no soporta 
multimodal nativamente) y automatizar la auditoría de calidad del sistema.

-----------------------------------

### ¿Qué es Whisper?
Modelo de OpenAI para **Speech-to-Text** (STT). Convierte audio en texto con alta 
precisión en múltiples idiomas. Lo usamos en `audio_service.py`.

### ¿Qué es Base64?
Codificación que convierte datos binarios (imágenes) en texto ASCII. 
Los LLMs multimodales esperan las imágenes en este formato dentro de un data URL: 
`data:image/jpeg;base64,<cadena>`.

### ¿Qué es Tool Calling?
Capacidad del LLM de invocar funciones externas (APIs, calculadoras, búsquedas). 
No lo usamos aún, pero LangGraph lo habilitaría en una próxima iteración.