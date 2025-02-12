import sys
import random
import repository as repo
from cli import input_str, input_yes_no, input_optional_int, input_optional_float


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
    best = []
    worst = []
    best_rating = None
    worst_rating = None

    for title, movie in movies.items():
        rating = movie["rating"]

        if best_rating is None or rating > best_rating:
            best_rating = rating

        if worst_rating is None or rating < worst_rating:
            worst_rating = rating

        ratings.append(rating)

    for title, movie in movies.items():
        rating = movie["rating"]

        if rating == best_rating:
            best.append(title)

        if rating == worst_rating:
            worst.append(title)

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
    print(f"Best movie(s): {', '.join(best)}, {best_rating}")
    print(f"Worst movie(s): {', '.join(worst)}, {worst_rating}")


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
    movies = repo.get_movies()
    latest_first = input_yes_no("Do you want the latest movies first?")
    sorted_movies = sorted(movies, key=lambda title: movies[title]["year"], reverse=latest_first)
    print()

    # TODO: make function to print movies
    for title in sorted_movies:
        movie = movies[title]
        print(f"{title} ({movie['year']}): {movie['rating']}")


def filter_movies():
    movies = repo.get_movies()

    min_rating = input_optional_float("Enter minimum rating (leave blank for no minimum rating): ",
                                      error_message="Please enter a valid rating")

    start_year = input_optional_int("Enter start year (leave blank for no start year): ",
                                    error_message="Please enter a valid start year")

    end_year = input_optional_int("Enter end year (leave blank for no end year): ",
                                  error_message="Please enter a valid end year")

    filtered_movies = []

    for title, movie in movies.items():
        rating = movie["rating"]
        year = movie["year"]

        has_min_rating = not min_rating or rating >= min_rating
        start_year_complies = not start_year or year >= start_year
        end_year_complies = not end_year or year <= end_year
        is_year_in_range = start_year_complies and end_year_complies

        if has_min_rating and is_year_in_range:
            filtered_movies.append(title)

    print()

    # TODO: make function to print movies
    for title in filtered_movies:
        movie = movies[title]
        print(f"{title} ({movie['year']}): {movie['rating']}")
