from flask import Blueprint, jsonify, request
from repository.sqlite_repository import repo
from omdb.omdb_client import OmdbClient
from environment import omdb_api_key

bp = Blueprint("api", __name__)


@bp.route("/movies")
def get_movies():
    title = request.args.get("title")

    if title:
        movies = repo.find_movies_like(title=title)
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
        except ValueError as error:
            return jsonify({"total_results": 0, "results": []})

    return "Bad Request", 400


def __jsonify_entities(entities):
    return jsonify({
        "total_results": len(entities),
        "results": [entity.to_dict() for entity in entities]
    })
