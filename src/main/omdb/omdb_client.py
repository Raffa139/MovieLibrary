import requests

OMDB_API = "https://www.omdbapi.com"


class OmdbClient:
    """
    A client for interacting with the OMDB API to retrieve movie information.
    """

    def __init__(self, *, api_key):
        """
        Initializes an OmdbClient object.

        Args:
            api_key (str): The API key for accessing the OMDB API.
        """
        self._api_key = api_key

    def find_movie_by_title(self, title):
        """
        Finds movie information by title using the OMDB API.

        Args:
            title (str): The title of the movie to search for.

        Returns:
            tuple: A tuple containing the movie's title, year, IMDb rating, poster URL, and IMDb ID.

        Raises:
            PermissionError: If the API key is invalid.
            RuntimeError: If an unexpected error occurs during the API request.
            ValueError: If the movie is not found.
        """
        url = f"{OMDB_API}?apikey={self._api_key}&type=movie&t={title}"
        response = requests.get(url)

        if response.status_code == 401:
            raise PermissionError("Invalid API-KEY")

        if not response.status_code == 200:
            raise RuntimeError(
                f"Unexpected error durnig movie fetching with code {response.status_code}")

        json = response.json()

        if "Error" in json:
            raise ValueError(f"Movie with title '{title}' not found")

        return {
            "title": json.get("Title"),
            "release_year": int(json.get("Year")),
            "rating": float(json.get("imdbRating")),
            "poster_url": json.get("Poster"),
            "imdb_id": json.get("imdbID"),
            "genres": json.get("Genre"),
            "directors": json.get("Director"),
            "writers": json.get("Writer"),
            "actors": json.get("Actors"),
        }

    def search_movies(self, title):
        url = f"{OMDB_API}?apikey={self._api_key}&type=movie&s={title}"
        response = requests.get(url)

        if response.status_code == 401:
            raise PermissionError("Invalid API-KEY")

        if not response.status_code == 200:
            raise RuntimeError(
                f"Unexpected error durnig movie fetching with code {response.status_code}")

        json = response.json()

        if "Error" in json:
            raise ValueError(f"Movie with title '{title}' not found or too many found")

        results = json.get("Search")
        total_results = json.get("totalResults")

        return {
            "total_results": total_results,
            "results": [{
                "title": result.get("Title"),
                "release_year": int(result.get("Year").replace("–", "")),
                "poster_url": result.get("Poster"),
                "imdb_id": result.get("imdbID")
            } for result in results]
        }
