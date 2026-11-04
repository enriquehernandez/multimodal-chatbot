# Problem Statement

## Contexto
En atención al cliente, soporte técnico y análisis de documentos visuales, los usuarios 
necesitan interactuar con sistemas de IA usando **voz e imágenes**, no solo texto. 
Un cliente puede enviar una foto de un producto dañado y preguntar "¿qué hago?", o 
un técnico puede dictar una consulta mientras revisa un manual visual.

Los LLMs de solo texto no resuelven esto: no "ven" ni "escuchan".

## Solución Propuesta
Desarrollar una API REST multimodal que:
- Acepte **texto, imágenes y audio** en una misma petición.
- Use un LLM multimodal (GPT-4o, Gemini, Llama Vision) para razonar sobre las tres modalidades.
- Sea **agnóstica al proveedor**: cambiar entre OpenAI, Azure OpenAI, Groq y Google 
  mediante una variable de entorno (Registry Pattern).
- Incluya **evaluación automática** (LLM-as-a-Judge) y **tests con mocks** para no 
  consumir tokens en CI/CD.