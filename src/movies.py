from repository.json_repository import JsonRepository
from app.movie_app import MovieApp


def main():
    """Initializes the movie repository and runs the main menu."""
    repo = JsonRepository("movies.json")
    app = MovieApp(repo)
    app.start()


if __name__ == "__main__":
    main()
