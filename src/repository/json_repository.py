import json
import os

from .irepository import IRepository


class JsonRepository(IRepository):
    def __init__(self, repository_file):
        super().__init__(repository_file)

    def initialize(self):
        if not os.path.exists(self._repository_file):
            with open(self._repository_file, "x"): pass

    def get_movies(self):
        return self._deserialize_movies()

    def get_movie_by_title(self, title):
        movies = self._deserialize_movies()

        if title not in movies:
            return None

        return movies[title]

    def has_movie(self, title):
        return self.get_movie_by_title(title) is not None

    def add_movie(self, title, year, rating):
        movies = self._deserialize_movies()

        movies[title] = {
            "rating": rating,
            "year": year
        }

        self._serialize_movies(movies)

    def delete_movie(self, title):
        movies = self._deserialize_movies()

        del movies[title]

        self._serialize_movies(movies)

    def update_movie(self, title, rating):
        movies = self._deserialize_movies()

        movies[title]["rating"] = rating

        self._serialize_movies(movies)

    def _serialize_movies(self, movies):
        with open(self._repository_file, "w") as file:
            content = json.dumps(movies)
            file.write(content)

    def _deserialize_movies(self):
        with open(self._repository_file) as file:
            content = file.read()

            if not content:
                return {}

            return json.loads(content)
