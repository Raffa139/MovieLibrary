from flask import Blueprint, render_template, request, redirect, url_for
from repository.sqlite_repository import repo

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    message = request.args.get("message")
    users = repo.find_all_users()
    return render_template("index.html", users=users, message=message)


@bp.route("/users/<int:user_id>")
def user_movies(user_id):
    message = request.args.get("message")
    user = repo.find_user_by_id(user_id)

    if not user:
        return "Not Found", 404

    return render_template("user_movies.html", user=user, user_movies=user.movies, message=message)


@bp.route("/users/<int:user_id>", methods=["POST"])
def add_user_movie(user_id):
    pass


@bp.route("/users/<int:user_id>/update-movie/<int:movie_id>")
def update_user_movie(user_id, movie_id):
    return redirect(
        url_for("main.user_movies", user_id=user_id, message="Movie updated successfully!"))


@bp.route("/users/<int:user_id>/delete-movie/<int:movie_id>")
def delete_user_movie(user_id, movie_id):
    return redirect(
        url_for("main.user_movies", user_id=user_id, message="Movie deleted successfully!"))
