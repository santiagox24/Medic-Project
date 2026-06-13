import openai
from config import OPENAI_API_KEY

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

async def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    Generates an embedding for the given text using OpenAI's API.
    By default uses text-embedding-3-small (1536 dimensions).
    """
    if not OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY is missing for embeddings.")
        return []

    if not text:
        return []
    
    # Replacing newlines as recommended by OpenAI
    text = text.replace("\n", " ")
    
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        
        response = await client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
