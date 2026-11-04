# Multimodal Chain Component

## Contrato de Entrada (API)
```json
{
  "texto": "¿Qué hay en esta imagen?",
  "imagen": "<archivo binario>",
  "audio": "<archivo binario>"
}
```

## Contrato de Salida
```json
{
  "answer": "string",
  "tokens_used": {
    "prompt_tokens": int,
    "completion_tokens": int,
    "total_tokens": int
  }
}
```

## Reglas de Negocio

1. **Al menos una modalidad**: La API rechaza peticiones vacías (400).
2. **Validación de imagen**: Se verifica con Pillow que sea una imagen real y no exceda 10 MB.
3. **Validación de audio**: Se verifica el MIME type y tamaño máximo de 25 MB.
4. **Fallo seguro**: Si Whisper falla, se devuelve 400 con mensaje claro.
5. **Atribución de tokens**: Se devuelven los tokens consumidos para auditoría de costos.
