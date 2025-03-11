import os
from abc import ABC, abstractmethod


class IRepository(ABC):
    def __init__(self, repository_file):
        self._repository_file = repository_file

    def initialize(self):
        """
        Initializes the movie repository by creating the movies.json file if it doesn't exist.
        """
        if not os.path.exists(self._repository_file):
            with open(self._repository_file, "x"): pass

    @abstractmethod
    def get_movies(self):
        """
        Returns a dictionary of dictionaries that contains the movies information in the database.
        The function loads the information from the JSON file and returns the data.

        Returns:
            dict: A dictionary of movie titles and their information.
        """
        pass

    @abstractmethod
    def get_movie_by_title(self, title):
        """
        Retrieves a movie's information by its title.

        Args:
            title (str): The title of the movie.

        Returns:
            dict or None: The movie's information as a dictionary, or None if the movie is not
            found.
        """
        pass

    @abstractmethod
    def has_movie(self, title):
        """
        Checks if a movie with the given title exists in the database.

        Args:
            title (str): The title of the movie.

        Returns:
            bool: True if the movie exists, False otherwise.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating):
        """
        Adds a movie to the movies database. Loads the information from the JSON file, adds the
        movie,
        and saves it.

        Args:
            title (str): The title of the movie.
            year (int): The year the movie was released.
            rating (float): The rating of the movie.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the movies database. Loads the information from the JSON file,
        deletes the movie, and saves it.

        Args:
            title (str): The title of the movie to delete.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the movies database. Loads the information from the JSON file,
        updates the movie, and saves it.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating of the movie.
        """
        pass

    @abstractmethod
    def _serialize_movies(self, movies):
        """
        Serializes the movies dictionary to the movies.json file.

        Args:
            movies (dict): The dictionary containing movie information.
        """
        pass

    @abstractmethod
    def _deserialize_movies(self):
        """
        Deserializes the movies.json file into a dictionary.

        Returns:
            dict: The dictionary containing movie information. Returns an empty dictionary if the
            file is empty.
        """
        pass
