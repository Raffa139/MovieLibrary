import os
from dotenv import load_dotenv


def omdb_api_key():
    """
    Loads environment variables from a .env file and returns the OMDb API key.

    Returns:
        str or None: The OMDb API key if found in the environment variables, otherwise None.
    """
    load_dotenv()
    return os.getenv("OMDb_API_KEY")


def gemini_api_key():
    """
    Loads environment variables from a .env file and returns the Gemini API key.

    Returns:
        str or None: The Gemini API key if found in the environment variables, otherwise None.
    """
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")


def database_uri():
    """
    Loads environment variables from a .env file and returns the database URI.

    Returns:
        str or None: The database URI if found in the environment variables, otherwise None.
    """
    load_dotenv()
    return os.getenv("DATABASE_URI")
