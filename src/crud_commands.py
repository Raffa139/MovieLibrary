import repository as repo
import views as view
from cli import input_str, input_int, input_float


def list_movies():
    movies = repo.get_movies()
    print(f"{len(movies)} movies in total:")
    view.movie_list(all_movies=movies, titles=movies.keys())


def add_movie():
    title = input_str("Enter new movie name: ", error_message="Please enter a valid title")

    if repo.has_movie(title):
        print(f"Movie {title} already exist!")
        return

    year = input_int("Enter new movie year: ", error_message="Please enter a valid year")
    rating = input_float("Enter new movie rating: ", error_message="Please enter a valid rating")
    repo.add_movie(title, year, rating)
    print(f"Movie {title} successfully added")


def update_movie():
    title = input_str("Enter movie name: ", error_message="Please enter a valid title")

    if not repo.has_movie(title):
        print(f"Movie {title} doesn't exist!")
        return

    rating = input_float("Enter new movie rating: ", error_message="Please enter a valid rating")
    repo.update_movie(title, rating)
    print(f"Movie {title} successfully updated")


def delete_movie():
    title = input_str("Enter movie name: ", error_message="Please enter a valid title")

    if not repo.has_movie(title):
        print(f"Movie {title} doesn't exist!")
        return

    repo.delete_movie(title)
    print(f"Movie {title} successfully deleted")
