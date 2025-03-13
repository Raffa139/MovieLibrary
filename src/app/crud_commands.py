import src.app.views as view
from src.app.cli import input_str, input_int, input_float


def list_movies(repo):
    """Lists all movies in the repository."""
    movies = repo.get_movies()
    print(f"{len(movies)} movies in total:")
    view.movie_list(all_movies=movies, titles=movies.keys())


def add_movie(repo, omdb_client):
    """Adds a new movie to the repository."""
    title = input_str("Enter new movie name: ", error_message="Please enter a valid title")

    if repo.has_movie(title):
        print(f"Movie {title} already exist!")
        return

    try:
        print(f"Searching for movie {title}... ", end="")
        full_title, year, rating, poster_url, imdb_id = omdb_client.find_movie(title)
        repo.add_movie(full_title, year, rating, poster_url, imdb_id)
        print(f"Movie {full_title} successfully added!")
    except ValueError:
        print(f"Movie with title {title} not found!")


def update_movie(repo):
    """Updates the rating of an existing movie."""
    title = input_str("Enter movie name: ", error_message="Please enter a valid title")

    if not repo.has_movie(title):
        print(f"Movie {title} doesn't exist!")
        return

    rating = input_float("Enter new movie rating: ", error_message="Please enter a valid rating")
    repo.update_movie(title, rating)
    print(f"Movie {title} successfully updated")


def delete_movie(repo):
    """Deletes a movie from the repository."""
    title = input_str("Enter movie name: ", error_message="Please enter a valid title")

    if not repo.has_movie(title):
        print(f"Movie {title} doesn't exist!")
        return

    repo.delete_movie(title)
    print(f"Movie {title} successfully deleted")
