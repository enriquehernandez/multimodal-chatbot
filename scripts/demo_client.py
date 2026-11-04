# scripts/demo_client.py
"""
Cliente de demostración para la API Multimodal Chatbot.

Este script prueba los 3 endpoints principales:
    1. GET  /health  → verifica que el servicio esté vivo.
    2. POST /chat    → texto + imagen.
    3. POST /chat    → texto + audio.
    4. POST /chat    → las tres modalidades juntas.

Uso:
    # Asegúrate de que el servidor esté corriendo en otra terminal:
    uv run uvicorn app.main:app --reload --port 8002

    # Luego ejecuta:
    uv run python scripts/demo_client.py

    # O con una URL personalizada:
    uv run python scripts/demo_client.py --url http://localhost:8002
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

import httpx

# Colores ANSI simples (sin dependencias externas)


class C:
    OK = "\033[92m"
    ERR = "\033[91m"
    INFO = "\033[94m"
    WARN = "\033[93m"
    BOLD = "\033[1m"
    END = "\033[0m"


# Rutas de ejemplo (relativas a la raíz del proyecto)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
IMAGEN_EJEMPLO = DATA_DIR / "images" / "laptop_bsod.png"
AUDIO_EJEMPLO = DATA_DIR / "audio" / "audio_soporte.mp3"


async def check_health(client: httpx.AsyncClient) -> bool:
    """Verifica que el servidor esté vivo."""
    print(f"\n{C.INFO}{C.BOLD}[1/4] GET /health{C.END}")
    try:
        r = await client.get("/health")
        r.raise_for_status()
        data = r.json()
        print(f"  {C.OK}✓ Servicio OK{C.END}")
        print(f"    Proveedor: {data.get('provider')}")
        print(f"    Modelo:    {data.get('model')}")
        return True
    except httpx.HTTPError as e:
        print(f"  {C.ERR}✗ Error: {e}{C.END}")
        return False


async def chat_texto_imagen(client: httpx.AsyncClient) -> None:
    """Prueba el endpoint /chat con texto + imagen."""
    print(f"\n{C.INFO}{C.BOLD}[2/4] POST /chat (texto + imagen){C.END}")

    if not IMAGEN_EJEMPLO.exists():
        print(
            f"  {C.WARN}⚠ No se encontró {IMAGEN_EJEMPLO}. Saltando prueba.{C.END}")
        return

    files = {"imagen": (IMAGEN_EJEMPLO.name,
                        IMAGEN_EJEMPLO.read_bytes(), "image/jpeg")}
    data = {"texto": "¿Qué hay en esta imagen?"}

    try:
        r = await client.post("/chat", data=data, files=files)
        r.raise_for_status()
        _print_response(r.json())
    except httpx.HTTPError as e:
        print(f"  {C.ERR}✗ Error: {e}{C.END}")
        if e.response is not None:
            print(f"    Detalle: {e.response.text}")


async def chat_texto_audio(client: httpx.AsyncClient) -> None:
    """Prueba el endpoint /chat con texto + audio."""
    print(f"\n{C.INFO}{C.BOLD}[3/4] POST /chat (texto + audio){C.END}")

    if not AUDIO_EJEMPLO.exists():
        print(f"  {C.WARN}⚠ No se encontró {AUDIO_EJEMPLO}. Saltando prueba.{C.END}")
        return

    files = {"audio": (AUDIO_EJEMPLO.name,
                       AUDIO_EJEMPLO.read_bytes(), "audio/mpeg")}
    data = {"texto": "Resume lo que digo en el audio"}

    try:
        r = await client.post("/chat", data=data, files=files)
        r.raise_for_status()
        _print_response(r.json())
    except httpx.HTTPError as e:
        print(f"  {C.ERR}✗ Error: {e}{C.END}")


async def chat_multimodal(client: httpx.AsyncClient) -> None:
    """Prueba el endpoint /chat con las tres modalidades."""
    print(
        f"\n{C.INFO}{C.BOLD}[4/4] POST /chat (texto + imagen + audio){C.END}")

    if not (IMAGEN_EJEMPLO.exists() and AUDIO_EJEMPLO.exists()):
        print(f"  {C.WARN}⚠ Faltan archivos de ejemplo. Saltando prueba.{C.END}")
        return

    files = {
        "imagen": (IMAGEN_EJEMPLO.name, IMAGEN_EJEMPLO.read_bytes(), "image/jpeg"),
        "audio": (AUDIO_EJEMPLO.name, AUDIO_EJEMPLO.read_bytes(), "audio/mpeg"),
    }
    data = {"texto": "¿Qué relación hay entre lo que digo y lo que ves?"}

    try:
        r = await client.post("/chat", data=data, files=files)
        r.raise_for_status()
        _print_response(r.json())
    except httpx.HTTPError as e:
        print(f"  {C.ERR}✗ Error: {e}{C.END}")


def _print_response(payload: dict) -> None:
    """Imprime la respuesta de forma legible."""
    tokens = payload.get("tokens_used", {})
    print(f"  {C.OK}✓ Respuesta recibida{C.END}")
    print(f"    {C.BOLD}Answer:{C.END} {payload.get('answer', '')}")
    print(
        f"    {C.BOLD}Tokens:{C.END} "
        f"{tokens.get('total_tokens', 0)} "
        f"(prompt={tokens.get('prompt_tokens', 0)}, "
        f"completion={tokens.get('completion_tokens', 0)})"
    )
    if "provider" in payload:
        print(f"    {C.BOLD}Provider:{C.END} {payload['provider']}")


async def main(url: str) -> int:
    """Ejecuta todas las pruebas y devuelve un código de salida."""
    print(f"{C.BOLD}=== Demo Client: Multimodal Chatbot API ==={C.END}")
    print(f"URL base: {url}")

    async with httpx.AsyncClient(base_url=url, timeout=120.0) as client:
        if not await check_health(client):
            print(f"\n{C.ERR}El servidor no responde. Abortando.{C.END}")
            return 1

        await chat_texto_imagen(client)
        await chat_texto_audio(client)
        await chat_multimodal(client)

    print(f"\n{C.OK}{C.BOLD}✓ Demo completada{C.END}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cliente demo para Multimodal Chatbot API")
    parser.add_argument(
        "--url",
        default="http://localhost:8002",
        help="URL base de la API (default: http://localhost:8002)",
    )
    args = parser.parse_args()

    try:
        sys.exit(asyncio.run(main(args.url)))
    except KeyboardInterrupt:
        print(f"\n{C.WARN}Interrumpido por el usuario.{C.END}")
        sys.exit(130)
