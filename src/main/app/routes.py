import os
from uuid import uuid4
from flask import Blueprint, render_template, request, redirect, url_for, abort, current_app as app
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
        return abort(404)

    return render_template(
        "user_movies.html",
        user=user,
        user_movies=user.movie_associations,
        start_recommendations=app.config.get("START_RECOMMENDATIONS"),
        movie_to_update=movie_to_update,
        current_rating=current_rating,
        msg=msg,
        msg_lvl=msg_lvl
    )


@bp.route("/users/<int:user_id>", methods=["POST"])
def add_user_movie(user_id):
    json = request.json
    movie_id = json.get("id")
    movie_title = json.get("title")

    if movie_title is None:
        return abort(400)

    if not repo.has_user(user_id):
        return abort(404)

    movie = repo.find_movie_by_title(movie_title)
    has_user_movie_by_id = repo.has_user_movie(user_id, movie_id)
    has_user_movie_by_title = movie and repo.has_user_movie(user_id, movie.id)
    user_has_movie_in_favourites = has_user_movie_by_id or has_user_movie_by_title

    if user_has_movie_in_favourites:
        return __redirect(
            "main.user_movies",
            ("Movie already in favourites!", "error"),
            user_id=user_id
        )

    try:
        movie_in_db = repo.has_movie(id=movie_id) or repo.has_movie(title=movie_title)
        if movie_in_db:
            repo.add_user_movie(user_id, movie_id or movie.id)
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

        return __redirect(
            "main.user_movies",
            ("Movie added successfully!", "success"),
            user_id=user_id
        )
    except Exception as e:
        app.logger.error(e)
        return abort(500)


@bp.route("/users/new", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template("add_user.html")

    username = request.form.get("username")
    profile_picture = request.files.get("profile_picture")
    profile_picture_file_name = None

    if not username:
        return abort(400)

    if profile_picture:
        if not __allowed_file_type(profile_picture):
            return render_template(
                "add_user.html",
                username=username,
                msg="Invalid file type of profile picture!",
                msg_lvl="error"
            )

        if not __allowed_file_size(profile_picture):
            return render_template(
                "add_user.html",
                username=username,
                msg="Profile picture too big! Max. 2MB",
                msg_lvl="error"
            )

        profile_picture_file_name = __store_file(profile_picture)

    try:
        repo.add_user(username, profile_picture_file_name)
        return __redirect("main.index", ("User created successfully!", "success"))
    except Exception as e:
        app.logger.error(e)
        return abort(500)


@bp.route("/users/<int:user_id>/update-movie/<int:movie_id>", methods=["GET", "POST"])
def update_user_movie(user_id, movie_id):
    if not repo.has_user(user_id):
        return abort(404)

    if not repo.has_movie(id=movie_id):
        return abort(404)

    if request.method == "GET":
        user_movie = repo.find_user_movie(user_id, movie_id)

        if not user_movie:
            return abort(404)

        current_rating = user_movie.personal_rating

        return __redirect(
            "main.user_movies",
            user_id=user_id,
            movie_to_update=movie_id,
            current_rating=current_rating
        )

    personal_rating = request.form.get("personal_rating")
    success = repo.update_user_movie(user_id, movie_id, personal_rating)
    msg = "Movie updated successfully!" if success else "Failed to update movie!"
    msg_lvl = "success" if success else "error"
    return __redirect("main.user_movies", (msg, msg_lvl), user_id=user_id)


@bp.route("/users/<int:user_id>/delete-movie/<int:movie_id>")
def delete_user_movie(user_id, movie_id):
    if not repo.has_user(user_id):
        return abort(404)

    if not repo.has_movie(id=movie_id):
        return abort(404)

    success = repo.delete_user_movie(user_id, movie_id)
    msg = "Movie deleted successfully!" if success else "Failed to deleted movie!"
    msg_lvl = "success" if success else "error"
    return __redirect("main.user_movies", (msg, msg_lvl), user_id=user_id)


@bp.app_errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400


@bp.app_errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@bp.app_errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


def __redirect(endpoint, message=(None, None), **kwargs):
    msg, msg_lvl = message
    return redirect(url_for(endpoint, msg=msg, msg_lvl=msg_lvl, **kwargs))


def __get_file_extension(filename):
    if not "." in filename:
        raise ValueError()
    return filename.split(".")[-1].lower()


def __store_file(file):
    extension = __get_file_extension(file.filename)
    filename = f"{str(uuid4())}.{extension}"
    filepath = os.path.join(app.config.get("UPLOADS_FOLDER"), filename)
    file.save(filepath)
    return filename


def __allowed_file_type(file):
    filename = file.filename

    try:
        return filename and __get_file_extension(filename) in app.config.get("ALLOWED_FILE_TYPES")
    except ValueError:
        return False


def __allowed_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= app.config.get("MAX_FILE_SIZE")
