from flask import Blueprint, jsonify, request, current_app as app
from repository.sqlite_repository import repo
from omdb.omdb_client import OmdbClient
from gemini.gemini_client import GeminiClient
from gemini.rate_limit_error import RateLimitError
from environment import omdb_api_key, gemini_api_key

bp = Blueprint("api", __name__)


@bp.route("/movies")
def get_movies():
    """
    Retrieves a list of movies from the local repository.

    Query Parameters:
        title (str, optional): If provided, filters movies whose title contains the given string
        (case-insensitive).

    Returns:
        jsonify: A JSON response containing a list of movies.
                 If a 'title' query parameter is provided, returns movies matching the title.
                 Otherwise, returns all movies in the repository.
    """
    title = request.args.get("title")

    if title:
        movies = repo.find_movies_like(title=title, limit=10)
        return __jsonify_entities(movies)

    movies = repo.find_all_movies()
    return __jsonify_entities(movies)


@bp.route("/omdb-movies")
def get_omdb_movies():
    """
    Retrieves movie information from the OMDB API based on a title.

    Query Parameters:
        title (str, required): The title of the movie to search for on OMDB.

    Returns:
        jsonify: A JSON response containing the search results from the OMDB API.
                 Returns a list of movies matching the title, including total results.
        tuple: A tuple containing a "Bad Request" message and a 400 status code if no title is
        provided.
    """
    omdb_client = OmdbClient(api_key=omdb_api_key())
    title = request.args.get("title")

    if title:
        try:
            movies = omdb_client.search_movies(title=title)
            return jsonify(movies)
        except ValueError:
            return jsonify({"total_results": 0, "results": []})

    return "Bad Request", 400


@bp.route("/users/<int:user_id>/recommendations")
def get_recommendations(user_id):
    """
    Retrieves movie recommendations for a specific user based on their favorite movies.

    Path Parameters:
        user_id (int): The ID of the user to get recommendations for.

    Returns:
        jsonify: A JSON response containing a list of recommended movie details fetched from OMDB.
                 Returns an empty list if the user has fewer than the required number of favorite
                 movies
                 to generate recommendations.
        tuple: A tuple containing a "Not Found" message and a 404 status code if the user with
        the given ID does not exist.
        tuple: A tuple containing an error message and a 401 status code if there is a permission
        error with the Gemini API.
        tuple: A tuple containing a "Too Many Requests" message and a 429 status code if the
        Gemini API rate limit is exceeded.
    """
    user = repo.find_user_by_id(user_id)

    if not user:
        return "Not Found", 404

    user_movies = user.movies
    if len(user_movies) < app.config.get("START_RECOMMENDATIONS"):
        return jsonify([])

    try:
        gemini_client = GeminiClient(api_key=gemini_api_key())
        omdb_client = OmdbClient(api_key=omdb_api_key())
        recommendations = gemini_client.find_recommendations([movie.title for movie in user_movies])

        movies = []
        for title in recommendations:
            try:
                movies.append(omdb_client.find_movie_by_title(title))
            except ValueError:
                continue  # Go on if movie not found

        return jsonify(movies)
    except PermissionError as e:
        return str(e), 401
    except RateLimitError:
        return "Too Many Requests", 429


def __jsonify_entities(entities):
    """
    Helper function to jsonify a list of SQLAlchemy entities.

    Args:
        entities (list): A list of SQLAlchemy entity objects.

    Returns:
        jsonify: A JSON response containing a list of dictionaries representing the entities.
    """
    return jsonify({
        "total_results": len(entities),
        "results": [entity.to_dict() for entity in entities]
    })
