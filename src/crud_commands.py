import repository as repo
from cli import input_int, input_float


def list_movies():
    movies = repo.get_movies()

    print(f"{len(movies)} movies in total:")

    for title, movie in movies.items():
        print(f"{title} ({movie['year']}): {movie['rating']}")


def add_movie():
    title = input("Enter new movie name: ")

    if repo.has_movie(title):
        print(f"Movie {title} already exist!")
        return

    year = input_int("Enter new movie year: ", error_message="Please enter a valid year")
    rating = input_float("Enter new movie rating: ", error_message="Please enter a valid rating")
    repo.add_movie(title, year, rating)
    print(f"Movie {title} successfully added")


def update_movie():
    title = input("Enter movie name: ")

    if not repo.has_movie(title):
        print(f"Movie {title} doesn't exist!")
        return

    rating = input_float("Enter new movie rating: ", error_message="Please enter a valid rating")
    repo.update_movie(title, rating)
    print(f"Movie {title} successfully updated")


def delete_movie():
    title = input("Enter movie name: ")

    if not repo.has_movie(title):
        print(f"Movie {title} doesn't exist!")
        return

    repo.delete_movie(title)
    print(f"Movie {title} successfully deleted")
