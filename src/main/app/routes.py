from flask import Blueprint, render_template, request, redirect, url_for
from repository.sqlite_repository import repo

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
    user = repo.find_user_by_id(user_id)

    if not user:
        return "Not Found", 404

    return render_template("user_movies.html", user=user, user_movies=user.movies, msg=msg,
                           msg_lvl=msg_lvl, movie_to_update=movie_to_update)


@bp.route("/users/<int:user_id>", methods=["POST"])
def add_user_movie(user_id):
    pass


@bp.route("/users/<int:user_id>/update-movie/<int:movie_id>", methods=["GET", "POST"])
def update_user_movie(user_id, movie_id):
    if request.method == "GET":
        return redirect(url_for("main.user_movies", user_id=user_id, movie_to_update=movie_id))

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
