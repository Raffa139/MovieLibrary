from flask import Blueprint, jsonify, request, current_app as app
from repository.sqlite_repository import repo
from omdb.omdb_client import OmdbClient
from gemini.gemini_client import GeminiClient
from gemini.rate_limit_error import RateLimitError
from environment import omdb_api_key, gemini_api_key

bp = Blueprint("api", __name__)


@bp.route("/movies")
def get_movies():
    title = request.args.get("title")

    if title:
        movies = repo.find_movies_like(title=title, limit=10)
        return __jsonify_entities(movies)

    movies = repo.find_all_movies()
    return __jsonify_entities(movies)


@bp.route("/omdb-movies")
def get_omdb_movies():
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
    return jsonify({
        "total_results": len(entities),
        "results": [entity.to_dict() for entity in entities]
    })
