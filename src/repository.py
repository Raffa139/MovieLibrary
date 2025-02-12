import json
import os

MOVIES_FILE = "movies.json"


def initialize():
    if not os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, "x"): pass


def serialize_movies(movies):
    with open(MOVIES_FILE, "w") as file:
        content = json.dumps(movies)
        file.write(content)


def deserialize_movies():
    with open(MOVIES_FILE) as file:
        content = file.read()

        if not content:
            return {}

        return json.loads(content)


def get_movies():
    """
    Returns a dictionary of dictionaries that contains the movies information in the database.
    The function loads the information from the JSON file and returns the data.
    """

    return deserialize_movies()


def get_movie_by_title(title):
    movies = deserialize_movies()

    if title not in movies:
        return None

    return movies[title]


def has_movie(title):
    return get_movie_by_title(title) is not None


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database. Loads the information from the JSON file, add the movie,
    and saves it.
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
    """

    movies = deserialize_movies()

    del movies[title]

    serialize_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movies database. Loads the information from the JSON file,
    updates the movie, and saves it.
    """

    movies = deserialize_movies()

    movies[title]["rating"] = rating

    serialize_movies(movies)
