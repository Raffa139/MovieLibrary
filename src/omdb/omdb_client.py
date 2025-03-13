import requests

OMDB_API = "https://www.omdbapi.com"


class OmdbClient:
    def __init__(self, *, api_key):
        self._api_key = api_key

    def find_movie(self, title):
        url = f"{OMDB_API}?apikey={self._api_key}&t={title}"
        response = requests.get(url)

        if response.status_code == 401:
            raise PermissionError("Invalid API-KEY")

        if not response.status_code == 200:
            raise RuntimeError(
                f"Unexpected error durnig movie fetching with code {response.status_code}")

        json = response.json()

        if "Error" in json:
            raise ValueError(f"Movie with title '{title}' not found")

        return json["Title"], int(json["Year"]), float(json["imdbRating"]), json["Poster"], json["imdbID"]
