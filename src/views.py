def movie_list(*, all_movies, titles):
    for title in titles:
        movie = all_movies[title]
        print(f"{title} ({movie['year']}): {round(movie['rating'], 1)}")
