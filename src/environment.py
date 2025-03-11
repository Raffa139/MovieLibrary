import os
from dotenv import load_dotenv


def get_api_key():
    """
    Retrieves the API key from environment variables.

    This function loads environment variables from a .env file using `load_dotenv()`
    and then retrieves the value of the "API_KEY" variable.

    Returns:
        str: The API key, or None if it is not set.
    """
    load_dotenv()
    return os.getenv("API_KEY")
