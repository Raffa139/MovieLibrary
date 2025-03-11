def movie_list(*, all_movies, titles):
    """
    Prints a formatted list of movies.

    Args:
        all_movies (dict): A dictionary containing movie titles as keys and movie data as values.
        titles (list[str]): A list of movie titles to display.
    """
    for title in titles:
        movie = all_movies[title]
        print(f"{title} ({movie['year']}): {round(movie['rating'], 1)}")
