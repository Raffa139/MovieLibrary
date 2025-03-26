from flask import Blueprint, render_template
from repository.sqlite_repository import repo

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    users = repo.find_all_users()
    return render_template("index.html", users=users)


@bp.route("/users/<int:user_id>")
def user_movies(user_id):
    user = repo.find_user_by_id(user_id)

    if not user:
        return "Not Found", 404

    return render_template("user_movies.html", user=user, user_movies=user.movies)


@bp.route("/users/<int:user_id>", methods=["POST"])
def add_user_movie(user_id):
    pass


@bp.route("/users/<int:user_id>/<int:movie_id>", methods=["UPDATE"])
def update_user_movie(user_id, movie_id):
    pass


@bp.route("/users/<int:user_id>/<int:movie_id>", methods=["DELETE"])
def delete_user_movie(user_id, movie_id):
    pass
