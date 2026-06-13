"""
Simple LLM wrapper for the app.
Reads `MODEL_NAME` and `OPENAI_API_KEY` from `app/config.py` (or `config.py` depending on runtime path).
Set environment variable `MODEL_NAME` to change the default model for all clients, e.g.

    export MODEL_NAME="gpt-5-mini"
    export OPENAI_API_KEY="sk-..."

Then call `generate_text(prompt)` to get completions.
"""

from openai import AsyncOpenAI
from config import MODEL_NAME, OPENAI_API_KEY

async def generate_text(prompt: str, model: str | None = None, max_tokens: int = 1024, temperature: float = 0.5) -> str:
    """Generate text using the configured model.
    Uses AsyncOpenAI client for version 1.0.0+.
    """
    if not OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY is missing. AI features will not work.")
        return "Servicio de IA no disponible (falta API Key)."

    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    model = model or MODEL_NAME
 
    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating text: {e}")
        return "Lo siento, hubo un error al procesar tu solicitud."

