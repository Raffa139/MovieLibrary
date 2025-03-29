from google.genai import Client
from google.genai.types import Content, Part, GenerateContentConfig, Schema, Type
from google.genai.errors import ClientError
from .rate_limit_error import RateLimitError


class GeminiClient:
    model = "gemini-2.0-flash"

    recommendation_restrictions = [
        "Give me exactly 5 suggestions for movies based on the list of favourite movies.",
        "Each suggestion should only contain the english movie title.",
        "Only reference real and existing movies.",
        "None of the movies from the favourites list should appear in the suggestions."
    ]

    def __init__(self, *, api_key):
        self._client = Client(api_key=api_key)

    def find_recommendations(self, favourite_titles):
        favourite_list = "\n".join([f"- {title}" for title in favourite_titles])
        restrictions = "\n".join(GeminiClient.recommendation_restrictions)
        prompt = f"Favourite movies:\n{favourite_list}\n\n{restrictions}"

        contents = [
            Content(role="user", parts=[Part.from_text(text=prompt)])
        ]

        content_config = GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Schema(
                type=Type.OBJECT,
                required=["titles"],
                properties={
                    "titles": Schema(
                        type=Type.ARRAY,
                        items=Schema(type=Type.STRING)
                    )
                }
            )
        )

        try:
            response = self._client.models.generate_content(
                model=GeminiClient.model, contents=contents, config=content_config
            )
            return response.parsed.get("titles", [])
        except ClientError as e:
            if e.code == 429:
                raise RateLimitError()

            if e.code == 400:
                raise PermissionError(e.message)

            raise e
