import sys
from repository.json_repository import JsonRepository
from repository.csv_repository import CsvRepository
from omdb.omdb_client import OmdbClient
from app.movie_app import MovieApp
from environment import get_api_key


def instantiate_repository():
    """
    Instantiates the movie repository based on command-line arguments.

    Returns:
        JsonRepository or CsvRepository: The instantiated repository object.
    """
    if len(sys.argv) < 2:
        return JsonRepository("movies.json")

    _, repo_file = sys.argv
    _, repo_file_type = repo_file.split(".")

    if repo_file_type.lower() == "json":
        return JsonRepository(repo_file)
    elif repo_file_type.lower() == "csv":
        return CsvRepository(repo_file)
    else:
        print(f"Repository file of type {repo_file_type} not supported.")
        sys.exit()


def main():
    """Initializes the movie repository and runs the MovieApp application."""
    repo = instantiate_repository()
    omdb_client = OmdbClient(api_key=get_api_key())
    app = MovieApp(repo, omdb_client)
    app.start()


if __name__ == "__main__":
    main()
