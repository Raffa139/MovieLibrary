from flask import Blueprint, render_template
from repository.sqlite_repository import repo

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    movies = repo.find_all_movies()
    return render_template("index.html", movies=movies)
