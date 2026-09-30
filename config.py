import os

from dotenv import load_dotenv


load_dotenv()


APP_NAME = os.getenv("APP_NAME", "EduGenie")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()


def validate_settings() -> None:
    """
    Validate required application configuration.

    The API key is checked when an AI endpoint is called rather than when
    the FastAPI application starts. This allows /health and the frontend
    to load even before the user configures Gemini.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Create a .env file and add your Gemini API key."
        )