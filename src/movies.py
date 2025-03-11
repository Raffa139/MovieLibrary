from repository.json_repository import JsonRepository
from omdb.omdb_client import OmdbClient
from app.movie_app import MovieApp
from environment import get_api_key


def main():
    """Initializes the movie repository and runs the main menu."""
    repo = JsonRepository("movies.json")
    omdb_client = OmdbClient(api_key=get_api_key())
    app = MovieApp(repo, omdb_client)
    app.start()


if __name__ == "__main__":
    main()
