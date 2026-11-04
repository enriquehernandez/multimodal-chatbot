# Evaluation Plan & Results (LLM-as-a-Judge)

Dado que Ragas no soporta multimodal nativamente, implementamos un pipeline 
de evaluación con **LLM-as-a-Judge** en `scripts/evaluate.py`.

## 📊 Resultados de la Última Evaluación

| Caso | Pregunta | Ground Truth | Score | Estado |
| :--- | :--- | :--- | :--- | :--- |
| 1 | ¿De qué color es el coche? | rojo | 1.0 | ✅ |
| 2 | ¿Cuántas personas hay? | 3 | 1.0 | ✅ |
| 3 | ¿Qué dice el audio? | "hola mundo" | 1.0 | ✅ |

*(Nota: los resultados son ilustrativos; se actualizan al correr el script.)*

## 🛠️ Plan de Mejoras
1. **Ampliar el dataset** de evaluación a 50+ casos con imágenes reales.
2. **Añadir métricas de latencia** por modalidad (STT, codificación, LLM).
3. **Comparar proveedores:** correr la evaluación contra OpenAI, Azure y Groq para 
   medir diferencias de calidad y costo.