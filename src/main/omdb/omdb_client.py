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
        Finds detailed movie information by title using the OMDB API.

        Args:
            title (str): The title of the movie to search for.

        Returns:
            dict: A dictionary containing the movie's title, release year, IMDb rating, poster URL,
                  IMDb ID, genres, directors, writers, and actors.

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

        return self.__sanitize_dict({
            "title": json.get("Title"),
            "release_year": self.__sanitize_year(json.get("Year")),
            "rating": float(json.get("imdbRating")),
            "poster_url": json.get("Poster"),
            "imdb_id": json.get("imdbID"),
            "genres": json.get("Genre").split(","),
            "directors": json.get("Director").split(","),
            "writers": json.get("Writer").split(","),
            "actors": json.get("Actors").split(","),
        })

    def search_movies(self, title):
        """
        Searches for movies by title using the OMDB API.

        Args:
            title (str): The title to search for.

        Returns:
            dict: A dictionary containing the total number of results and a list of matching movies,
                  each with title, release year, poster URL, and IMDb ID.

        Raises:
            PermissionError: If the API key is invalid.
            RuntimeError: If an unexpected error occurs during the API request.
            ValueError: If no movies are found for the given title or too many are found.
        """
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
            "results": [self.__sanitize_dict({
                "title": result.get("Title"),
                "release_year": self.__sanitize_year(result.get("Year")),
                "poster_url": result.get("Poster"),
                "imdb_id": result.get("imdbID")
            }) for result in results]
        }

    def __sanitize_dict(self, dict):
        """
        Sanitizes string values within a dictionary by stripping leading/trailing whitespace
        and recursively sanitizing lists and tuples.

        Args:
            dict (dict): The dictionary to sanitize.

        Returns:
            dict: The sanitized dictionary.
        """
        sanitized_dict = {**dict}
        for key, value in dict.items():
            if isinstance(value, str):
                sanitized_dict[key] = self.__sanitize_field(value)

            if isinstance(value, (list, tuple)):
                sanitized_dict[key] = self.__sanitize_fields(value)

        return sanitized_dict

    def __sanitize_field(self, value):
        """
        Sanitizes a single string value by stripping leading/trailing whitespace.

        Args:
            value (str): The string value to sanitize.

        Returns:
            str: The sanitized string value.
        """
        return value.strip()

    def __sanitize_fields(self, values):
        """
        Sanitizes a list or tuple of string values.

        Args:
            values (list or tuple): The list or tuple of string values to sanitize.

        Returns:
            list: A list containing the sanitized string values.
        """
        return [self.__sanitize_field(value) for value in values]

    def __sanitize_year(self, year):
        """
        Sanitizes a year string by stripping whitespace and replacing '–' with '' before
        converting to an integer.

        Args:
            year (str): The year string to sanitize.

        Returns:
            int: The sanitized year as an integer.
        """
        return int(self.__sanitize_field(year).replace("–", ""))
