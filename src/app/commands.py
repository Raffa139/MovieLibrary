import sys
import random
import app.views as view
import webgen.movie_html_generator as web_gen
from app.cli import input_str, input_yes_no, input_optional_int, input_optional_float


def exit_program():
    """Exits the program."""
    print("Bye!")
    sys.exit()


def stats(repo):
    """Calculates and displays movie statistics."""
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

    if has_odd_number_movies:
        median = sorted_ratings[number_movies // 2]
    else:
        first_middle = sorted_ratings[number_movies // 2]
        second_middle = sorted_ratings[(number_movies // 2) - 1]
        median = sum((first_middle, second_middle)) / 2

    print(f"Average rating: {round(avg, 1)}")
    print(f"Median rating: {round(median, 1)}")
    print(f"Best movie(s): {', '.join(best)}, {round(best_rating, 1)}")
    print(f"Worst movie(s): {', '.join(worst)}, {round(worst_rating, 1)}")


def random_movie(repo):
    """Selects and displays a random movie."""
    movies = repo.get_movies()
    title, movie = random.choice(list(movies.items()))
    print(f"Your movie for tonight: {title}, it's rated {round(movie['rating'], 1)}")


def search_movie(repo):
    """Searches for movies by name and displays the results."""
    movies = repo.get_movies()
    search = input_str("Enter part of movie name: ", error_message="Please enter a valid part")
    found_titles = [title for title in movies if search.lower() in title.lower()]
    print()
    view.movie_list(all_movies=movies, titles=found_titles)


def sorted_by_rating(repo):
    """Displays movies sorted by rating."""
    movies = repo.get_movies()
    sorted_movies = sorted(movies, key=lambda title: movies[title]["rating"], reverse=True)
    view.movie_list(all_movies=movies, titles=sorted_movies)


def sorted_by_year(repo):
    """Displays movies sorted by year, with options for latest or oldest first."""
    movies = repo.get_movies()
    latest_first = input_yes_no("Do you want the latest movies first?")
    sorted_movies = sorted(movies, key=lambda title: movies[title]["year"], reverse=latest_first)
    print()
    view.movie_list(all_movies=movies, titles=sorted_movies)


def filter_movies(repo):
    """Filters and displays movies based on rating and year criteria."""
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
    view.movie_list(all_movies=movies, titles=filtered_movies)


def generate_website(repo):
    """Generates a website with the movies from the repository."""
    movies = repo.get_movies()
    web_gen.generate_website(movies)
