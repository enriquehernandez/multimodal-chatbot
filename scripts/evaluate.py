# scripts/evaluate.py
"""
Pipeline de evaluación LLM-as-a-Judge.
"""
import asyncio
import csv
import logging
import re
import sys
from pathlib import Path

from langchain_core.messages import HumanMessage

from app.core.config import settings
from app.core.llm_factory import get_llm
from app.services.multimodal_engine import MultimodalEngine

logging.basicConfig(level=logging.WARNING,
                    format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Rutas de archivos
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
IMAGEN_EJEMPLO = DATA_DIR / "images" / "laptop_bsod.png"
AUDIO_EJEMPLO = DATA_DIR / "audio" / "audio_soporte.mp3"
CSV_OUTPUT = Path(__file__).resolve().parent.parent / "evaluation_results.csv"

# Set de pruebas
CASOS = [
    {
        "id": "test_01",
        "tipo": "imagen",
        "archivo": IMAGEN_EJEMPLO,
        "pregunta": "¿Qué problema se ve en la imagen?",
        "ground_truth": "Una pantalla azul de la muerte (BSOD) de Windows.",
    },
    {
        "id": "test_02",
        "tipo": "audio",
        "archivo": AUDIO_EJEMPLO,
        "pregunta": "¿Qué necesita el usuario?",
        "ground_truth": "Ayuda urgente con su laptop porque tiene una entrega.",
    }
]

PROMPT_JUEZ = """Eres un evaluador experto. Evalúa la respuesta de un asistente basándote en la verdad esperada.
Pregunta: {pregunta}
Respuesta del Asistente: {respuesta}
Verdad Esperada: {ground_truth}

Asigna un puntaje de 0 a 10. Responde ÚNICAMENTE con el número entero, sin texto adicional."""


async def evaluar_respuesta(llm, pregunta, respuesta, ground_truth) -> float:
    """Usa el LLM como juez para puntuar la respuesta."""
    prompt = PROMPT_JUEZ.format(
        pregunta=pregunta,
        respuesta=respuesta,
        ground_truth=ground_truth
    )
    try:
        res = await llm.ainvoke([HumanMessage(content=prompt)])
        # Buscamos el primer número en la respuesta del LLM (por si acaso devuelve "Puntaje: 10")
        match = re.search(r'\b(10|[0-9](?:\.\d+)?)\b', res.content)
        if match:
            return float(match.group(1))
        return 0.0
    except Exception as e:
        logger.error(f"Error al evaluar con el LLM: {e}")
        return 0.0


async def main():
    print(f"\n{'='*50}")
    print(" 🚀 INICIANDO EVALUACIÓN (LLM-as-a-Judge)")
    print(f"{'='*50}\n")
    print(
        f"🤖 Proveedor LLM: {settings.LLM_PROVIDER} ({settings.get_active_llm_model()})\n")

    engine = MultimodalEngine()
    llm_juez = get_llm()

    resultados = []

    for caso in CASOS:
        print(f"Evaluando caso [{caso['id']}] - {caso['pregunta']}")

        if not caso["archivo"].exists():
            print(
                f"  ⚠️ [OMITIDO] No se encontró el archivo: {caso['archivo']}")
            continue

        bytes_data = caso["archivo"].read_bytes()

        try:
            if caso["tipo"] == "imagen":
                res_engine = await engine.procesar(texto=caso["pregunta"], imagen_bytes=bytes_data)
            elif caso["tipo"] == "audio":
                res_engine = await engine.procesar(texto=caso["pregunta"], audio_bytes=bytes_data)
            else:
                continue

            respuesta = res_engine["answer"]
            print(f"  💬 Respuesta: {respuesta[:80]}...")

            print("  ⚖️  Evaluando con LLM-as-a-Judge...")
            score = await evaluar_respuesta(llm_juez, caso["pregunta"], respuesta, caso["ground_truth"])
            print(f"  ✅ Puntaje: {score}/10\n")

            resultados.append({
                "id": caso["id"],
                "tipo": caso["tipo"],
                "pregunta": caso["pregunta"],
                "respuesta_generada": respuesta,
                "ground_truth": caso["ground_truth"],
                "score": score
            })

        except Exception as e:
            logger.error(f"  ❌ Error procesando caso: {e}\n")
            resultados.append({
                "id": caso["id"],
                "tipo": caso["tipo"],
                "pregunta": caso["pregunta"],
                "respuesta_generada": "ERROR",
                "ground_truth": caso["ground_truth"],
                "score": 0.0
            })

    if resultados:
        with open(CSV_OUTPUT, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
            writer.writeheader()
            writer.writerows(resultados)
        print(f"{'='*50}")
        print(f"📊 Resultados guardados en: {CSV_OUTPUT.name}")

        promedio = sum(r["score"] for r in resultados) / len(resultados)
        print(f"🌟 Puntuación Promedio: {promedio:.2f}/10")
        print(f"{'='*50}\n")
    else:
        print("No se generaron resultados.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nEvaluación cancelada por el usuario.")
        sys.exit(130)
