"""
Simple LLM wrapper for the app.
Reads `MODEL_NAME` and `OPENAI_API_KEY` from `app/config.py` (or `config.py` depending on runtime path).
Set environment variable `MODEL_NAME` to change the default model for all clients, e.g.

    export MODEL_NAME="gpt-5-mini"
    export OPENAI_API_KEY="sk-..."

Then call `generate_text(prompt)` to get completions.
"""

try:
    import openai
except Exception:
    openai = None

# Import config the same way other modules do in this project
from config import MODEL_NAME, OPENAI_API_KEY

if openai and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


def generate_text(prompt: str, model: str | None = None, max_tokens: int = 512, temperature: float = 0.7) -> str:
    """Generate text using the configured model.

    - Uses `model` if provided, otherwise uses `MODEL_NAME` from config.
    - Raises a RuntimeError if the `openai` package is not installed.
    """
    model = model or MODEL_NAME

    if openai is None:
        raise RuntimeError("`openai` package not installed. Install with `pip install openai`.")

    # Prefer Chat Completions (for chat-style models like gpt-5-mini), fall back to Completion
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].message.content
    except Exception:
        # Try completion endpoint as fallback
        resp = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return resp.choices[0].text
