import sys
import random
import repository as repo
from cli import input_str


def exit_program():
    print("Bye!")
    sys.exit()


def stats():
    movies = repo.get_movies()
    number_movies = len(movies)
    has_odd_number_movies = number_movies % 2 == 1

    if number_movies == 0:
        return

    ratings = []
    best = None  # make list
    worst = None  # make list
    best_rating = None  # make list
    worst_rating = None  # make list

    for title, movie in movies.items():
        rating = movie["rating"]

        if best_rating is None or rating > best_rating:
            best_rating = rating
            best = title

        if worst_rating is None or rating < worst_rating:
            worst_rating = rating
            worst = title

        ratings.append(rating)

    avg = sum(ratings) / number_movies
    sorted_ratings = sorted(ratings)
    median = 0

    if has_odd_number_movies:
        median = sorted_ratings[number_movies // 2]
    else:
        first_middle = sorted_ratings[number_movies // 2]
        second_middle = sorted_ratings[(number_movies // 2) - 1]
        median = sum((first_middle, second_middle)) / 2

    print(f"Average rating: {round(avg, 1)}")
    print(f"Median rating: {round(median, 1)}")
    print(f"Best movie: {best}, {best_rating}")
    print(f"Worst movie: {worst}, {worst_rating}")


def random_movie():
    movies = repo.get_movies()
    title, movie = random.choice(list(movies.items()))
    print(f"Your movie for tonight: {title}, it's rated {movie['rating']}")


def search_movie():
    movies = repo.get_movies()
    search = input_str("Enter part of movie name: ", error_message="Please enter a valid part")
    found_titles = [title for title in movies if search.lower() in title.lower()]

    for title in found_titles:
        movie = movies[title]
        print(f"{title}, {movie['rating']}")


def sorted_by_rating():
    movies = repo.get_movies()
    sorted_movies = sorted(movies, key=lambda title: movies[title]["rating"], reverse=True)

    for title in sorted_movies:
        movie = movies[title]
        print(f"{title} ({movie['year']}): {movie['rating']}")


def sorted_by_year():
    pass


def filter_movies():
    pass
