# Vision and Goals

## Visión
Crear una API multimodal de nivel producción que cualquier empresa pueda desplegar 
para sus flujos de atención al cliente, soporte técnico o análisis de documentos.

## Objetivos Técnicos
1. **Multimodalidad real:** Texto + imagen + audio en una sola llamada.
2. **Provider-Agnostic:** Registry Pattern para OpenAI, Azure OpenAI, Groq y Google.
3. **Seguridad:** Validación de MIME types, límites de tamaño, cero hardcoding de API keys.
4. **Calidad Medible:** Pipeline de evaluación con LLM-as-a-Judge.
5. **Testing:** Mocks de LLM, Whisper y validación de imágenes. Cobertura 100% en `app/`.