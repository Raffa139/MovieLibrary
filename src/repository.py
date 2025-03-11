import json
import os

MOVIES_FILE = "movies.json"


def initialize():
    """
    Initializes the movie repository by creating the movies.json file if it doesn't exist.
    """
    if not os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, "x"): pass


def serialize_movies(movies):
    """
    Serializes the movies dictionary to the movies.json file.

    Args:
        movies (dict): The dictionary containing movie information.
    """
    with open(MOVIES_FILE, "w") as file:
        content = json.dumps(movies)
        file.write(content)


def deserialize_movies():
    """
    Deserializes the movies.json file into a dictionary.

    Returns:
        dict: The dictionary containing movie information. Returns an empty dictionary if the
        file is empty.
    """
    with open(MOVIES_FILE) as file:
        content = file.read()

        if not content:
            return {}

        return json.loads(content)


def get_movies():
    """
    Returns a dictionary of dictionaries that contains the movies information in the database.
    The function loads the information from the JSON file and returns the data.

    Returns:
        dict: A dictionary of movie titles and their information.
    """
    return deserialize_movies()


def get_movie_by_title(title):
    """
    Retrieves a movie's information by its title.

    Args:
        title (str): The title of the movie.

    Returns:
        dict or None: The movie's information as a dictionary, or None if the movie is not found.
    """
    movies = deserialize_movies()

    if title not in movies:
        return None

    return movies[title]


def has_movie(title):
    """
    Checks if a movie with the given title exists in the database.

    Args:
        title (str): The title of the movie.

    Returns:
        bool: True if the movie exists, False otherwise.
    """
    return get_movie_by_title(title) is not None


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database. Loads the information from the JSON file, adds the movie,
    and saves it.

    Args:
        title (str): The title of the movie.
        year (int): The year the movie was released.
        rating (float): The rating of the movie.
    """
    movies = deserialize_movies()

    movies[title] = {
        "rating": rating,
        "year": year
    }

    serialize_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database. Loads the information from the JSON file,
    deletes the movie, and saves it.

    Args:
        title (str): The title of the movie to delete.
    """
    movies = deserialize_movies()

    del movies[title]

    serialize_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie's rating in the movies database. Loads the information from the JSON file,
    updates the movie, and saves it.

    Args:
        title (str): The title of the movie to update.
        rating (float): The new rating of the movie.
    """
    movies = deserialize_movies()

    movies[title]["rating"] = rating

    serialize_movies(movies)
