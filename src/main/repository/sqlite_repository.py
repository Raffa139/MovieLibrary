from sqlalchemy.exc import NoResultFound
from .irepository import IRepository
from .entities import Movie, Genre, CrewMember, User
from . import db


class SQLiteRepository(IRepository):
    def find_all_movies(self):
        return Movie.query.all()

    def find_movie_by_id(self, id):
        try:
            return Movie.query.filter(Movie.id == id).one()
        except NoResultFound:
            return None

    def find_movie_by_title(self, title):
        return Movie.query.filter(Movie.title == title).all()

    def has_movie(self, id):
        return self.find_movie_by_id(id) is not None

    def add_movie(self, title, release_year, rating, poster_url, imdb_id):
        movie = Movie(title=title,
                      release_year=release_year,
                      rating=rating,
                      poster_url=poster_url,
                      imdb_id=imdb_id)

        db.session.add(movie)
        db.session.commit()

    def add_genre(self, name):
        genre = Genre(name=name)
        db.session.add(genre)
        db.session.commit()

    def add_crew_member(self, full_name):
        crew_member = CrewMember(full_name=full_name)
        db.session.add(crew_member)
        db.session.commit()

    def add_user(self, username):
        user = User(username=username)
        db.session.add(user)
        db.session.commit()

    def find_all_users(self):
        return User.query.all()

    def find_user_by_id(self, id):
        try:
            return User.query.filter(User.id == id).one()
        except NoResultFound:
            return None

    def find_user_movies(self):
        pass

    def delete_user_movie(self, id):
        pass

    def update_user_movie(self, id, personal_rating):
        pass


sqlite_repo = SQLiteRepository()
