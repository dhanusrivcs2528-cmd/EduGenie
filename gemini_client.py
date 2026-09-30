from typing import Optional, Type, TypeVar

from google import genai
from pydantic import BaseModel

from config import GEMINI_API_KEY, GEMINI_MODEL


T = TypeVar("T", bound=BaseModel)


_client: Optional[genai.Client] = None


def get_client() -> genai.Client:
    """
    Create the Gemini client lazily.

    Lazy initialization means the application can start and expose
    /health even when the API key has not been configured yet.
    """
    global _client

    if _client is not None:
        return _client

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to the .env file."
        )

    _client = genai.Client(api_key=GEMINI_API_KEY)

    return _client


def generate_text(
    prompt: str,
    *,
    system_instruction: Optional[str] = None,
    temperature: float = 0.4,
    max_output_tokens: int = 2048,
) -> str:
    """
    Generate a normal text response from Gemini.
    """
    client = get_client()

    config = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }

    if system_instruction:
        config["system_instruction"] = system_instruction

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config,
    )

    text = response.text

    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return text.strip()


def generate_structured(
    prompt: str,
    response_model: Type[T],
    *,
    system_instruction: Optional[str] = None,
    temperature: float = 0.3,
    max_output_tokens: int = 4096,
) -> T:
    """
    Generate a response that follows a Pydantic schema.

    Gemini supports structured output using a JSON response schema.
    """
    client = get_client()

    config = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
        "response_mime_type": "application/json",
        "response_schema": response_model,
    }

    if system_instruction:
        config["system_instruction"] = system_instruction

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty structured response.")

    try:
        return response_model.model_validate_json(response.text)
    except Exception as exc:
        raise RuntimeError(
            f"Gemini returned invalid structured data: {exc}"
        ) from exc