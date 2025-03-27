from flask import Blueprint, render_template, request, redirect, url_for
from repository.sqlite_repository import repo
from omdb.omdb_client import OmdbClient
from environment import omdb_api_key

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    msg = request.args.get("msg")
    msg_lvl = request.args.get("msg_lvl")
    users = repo.find_all_users()
    return render_template("index.html", users=users, msg=msg, msg_lvl=msg_lvl)


@bp.route("/users/<int:user_id>")
def user_movies(user_id):
    msg = request.args.get("msg")
    msg_lvl = request.args.get("msg_lvl")
    movie_to_update = request.args.get("movie_to_update")
    current_rating = request.args.get("current_rating")

    user = repo.find_user_by_id(user_id)

    if not user:
        return "Not Found", 404

    return render_template("user_movies.html", user=user, user_movies=user.movies, msg=msg,
                           msg_lvl=msg_lvl, movie_to_update=movie_to_update,
                           current_rating=current_rating)


@bp.route("/users/<int:user_id>", methods=["POST"])
def add_user_movie(user_id):
    json = request.json
    movie_id = json.get("id")
    movie_title = json.get("title")

    if movie_title is None:
        return "Bad Request", 400

    if not repo.has_user(user_id):
        return "Not Found", 404

    movie = repo.find_movie_by_title(movie_title)
    if repo.has_user_movie(user_id, movie_id) or (movie and repo.has_user_movie(user_id, movie.id)):
        return redirect(
            url_for("main.user_movies", user_id=user_id, msg="Movie already in favourites!",
                    msg_lvl="error"))

    if repo.has_movie(id=movie_id) or repo.has_movie(title=movie_title):
        repo.add_user_movie(user_id, movie_id)
    else:
        omdb_client = OmdbClient(api_key=omdb_api_key())
        movie = omdb_client.find_movie_by_title(movie_title)

        new_movie = repo.add_movie(
            movie.get("title"),
            movie.get("release_year"),
            movie.get("rating"),
            movie.get("poster_url"),
            movie.get("imdb_id"),
            movie.get("genres"),
            movie.get("directors"),
            movie.get("writers"),
            movie.get("actors")
        )
        repo.add_user_movie(user_id, new_movie.id)

    return redirect(url_for("main.user_movies", user_id=user_id, msg="Movie added successfully!",
                            msg_lvl="success"))


@bp.route("/users/<int:user_id>/update-movie/<int:movie_id>", methods=["GET", "POST"])
def update_user_movie(user_id, movie_id):
    if request.method == "GET":
        user_movie = repo.find_user_movie(user_id, movie_id)

        if not user_movie:
            return "Not Found", 404

        current_rating = user_movie.personal_rating
        return redirect(url_for("main.user_movies", user_id=user_id, movie_to_update=movie_id,
                                current_rating=current_rating))

    personal_rating = request.form.get("personal_rating")
    success = repo.update_user_movie(user_id, movie_id, personal_rating)

    msg = "Movie updated successfully!"
    msg_lvl = "success"
    if not success:
        msg = "Failed to update movie!"
        msg_lvl = "error"

    return redirect(url_for("main.user_movies", user_id=user_id, msg=msg, msg_lvl=msg_lvl))


@bp.route("/users/<int:user_id>/delete-movie/<int:movie_id>")
def delete_user_movie(user_id, movie_id):
    success = repo.delete_user_movie(user_id, movie_id)

    msg = "Movie deleted successfully!"
    msg_lvl = "success"
    if not success:
        msg = "Failed to deleted movie!"
        msg_lvl = "error"

    return redirect(url_for("main.user_movies", user_id=user_id, msg=msg, msg_lvl=msg_lvl))
