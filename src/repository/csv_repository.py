import csv

from .irepository import IRepository


class CsvRepository(IRepository):
    def __init__(self, repository_file):
        super().__init__(repository_file)

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
        with open(self._repository_file, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)

            for title, movie in movies.items():
                writer.writerow([title, movie["rating"], movie["year"]])

    def _deserialize_movies(self):
        with open(self._repository_file, encoding="utf-8") as file:
            reader = csv.reader(file)
            movies = {}

            for row in reader:
                title, rating, year = row
                movies[title] = {
                    "rating": float(rating),
                    "year": int(year)
                }

            return movies
