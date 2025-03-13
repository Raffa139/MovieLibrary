import os
from abc import ABC, abstractmethod


class IRepository(ABC):
    """
    Abstract base class for movie repositories.
    """

    def __init__(self, repository_file):
        """
        Initializes an IRepository object.

        Args:
            repository_file (str): The path to the repository file.
        """
        self._repository_file = repository_file

    def initialize(self):
        """
        Initializes the movie repository by creating the repository file if it doesn't exist.
        """
        if not os.path.exists(self._repository_file):
            with open(self._repository_file, "x"): pass

    def get_movies(self):
        """
        Returns a dictionary of dictionaries that contains the movies information in the database.

        Returns:
            dict: A dictionary of movie titles and their information.
        """
        return self._deserialize_movies()

    def get_movie_by_title(self, title):
        """
        Retrieves a movie's information by its title.

        Args:
            title (str): The title of the movie.

        Returns:
            dict or None: The movie's information as a dictionary, or None if the movie is not
            found.
        """
        movies = self._deserialize_movies()

        if title not in movies:
            return None

        return movies[title]

    def has_movie(self, title):
        """
        Checks if a movie with the given title exists in the database.

        Args:
            title (str): The title of the movie.

        Returns:
            bool: True if the movie exists, False otherwise.
        """
        return self.get_movie_by_title(title) is not None

    def add_movie(self, title, year, rating, poster_url, imdb_id):
        """
        Adds a movie to the movies database.

        Args:
            title (str): The title of the movie.
            year (int): The year the movie was released.
            rating (float): The rating of the movie.
            poster_url (str): The URL of the movie poster.
            imdb_id (str): The IMDb ID of the movie.
        """
        movies = self._deserialize_movies()

        movies[title] = {
            "year": year,
            "rating": rating,
            "poster_url": poster_url,
            "imdb_id": imdb_id
        }

        self._serialize_movies(movies)

    def delete_movie(self, title):
        """
        Deletes a movie from the movies database.

        Args:
            title (str): The title of the movie to delete.
        """
        movies = self._deserialize_movies()

        del movies[title]

        self._serialize_movies(movies)

    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the movies database.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating of the movie.
        """
        movies = self._deserialize_movies()

        movies[title]["rating"] = rating

        self._serialize_movies(movies)

    @abstractmethod
    def _serialize_movies(self, movies):
        """
        Serializes the movies dictionary to the repository file.

        Args:
            movies (dict): The dictionary containing movie information.
        """
        pass

    @abstractmethod
    def _deserialize_movies(self):
        """
        Deserializes the repository file into a dictionary.

        Returns:
            dict: The dictionary containing movie information. Returns an empty dictionary if the
            file is empty.
        """
        pass
