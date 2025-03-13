import json

from repository.irepository import IRepository


class JsonRepository(IRepository):
    def __init__(self, repository_file):
        super().__init__(repository_file)

    def _serialize_movies(self, movies):
        with open(self._repository_file, mode="w", encoding="utf-8") as file:
            content = json.dumps(movies)
            file.write(content)

    def _deserialize_movies(self):
        with open(self._repository_file, encoding="utf-8") as file:
            content = file.read()

            if not content:
                return {}

            return json.loads(content)
