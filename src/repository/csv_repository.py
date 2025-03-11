import csv

from .irepository import IRepository


class CsvRepository(IRepository):
    def __init__(self, repository_file):
        super().__init__(repository_file)

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
