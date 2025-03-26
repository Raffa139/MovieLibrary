from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from .irepository import IRepository
from .entities import Movie, Genre, CrewMember, User, MovieCrewMemberAssociation, \
    MovieUserAssociation
from . import db


class SQLiteRepository(IRepository):
    def find_all_movies(self):
        return Movie.query.all()

    def find_movie_by_id(self, id):
        try:
            return Movie.query.filter(Movie.id == id).one()
        except NoResultFound:
            return None

    def find_movies_by_title(self, title):
        return Movie.query.filter(Movie.title == title).all()

    def find_movies_like(self, title):
        return Movie.query.filter(Movie.title.ilike(f"%{title}%")).all()

    def has_movie(self, id):
        return self.find_movie_by_id(id) is not None

    def add_movie(self, title, release_year, rating, poster_url, imdb_id, genre_names, directors,
                  writers, actors):
        genres = []
        for genre_name in genre_names:
            genre = self.find_genre_by_name(genre_name)

            if not genre:
                new_genre = self.add_genre(genre_name)
                genres.append(new_genre)
            else:
                genres.append(genre)

        try:
            movie = Movie(title=title,
                          release_year=release_year,
                          rating=rating,
                          poster_url=poster_url,
                          imdb_id=imdb_id,
                          genres=genres)

            db.session.add(movie)
            db.session.flush()
        except SQLAlchemyError:
            db.session.rollback()

        director_associations = [
            self.__create_movie_crew_member_association(director, movie.id, member_type="director")
            for director in directors]

        writer_associations = [
            self.__create_movie_crew_member_association(writer, movie.id, member_type="writer")
            for writer in writers]

        actor_associations = [
            self.__create_movie_crew_member_association(actor, movie.id, member_type="actor")
            for actor in actors]

        try:
            db.session.add_all(director_associations)
            db.session.add_all(writer_associations)
            db.session.add_all(actor_associations)
            db.session.commit()
            return Movie.query.filter(Movie.id == movie.id).one()
        except SQLAlchemyError:
            db.session.rollback()

    def add_genre(self, name):
        genre = Genre(name=name)

        try:
            db.session.add(genre)
            db.session.commit()
            return Genre.query.filter(Genre.id == genre.id).one()
        except SQLAlchemyError:
            db.session.rollback()

    def find_genre_by_name(self, name):
        try:
            return Genre.query.filter(Genre.name == name).one()
        except NoResultFound:
            return None

    def add_crew_member(self, full_name):
        crew_member = CrewMember(full_name=full_name)

        try:
            db.session.add(crew_member)
            db.session.commit()
            return CrewMember.query.filter(CrewMember.id == crew_member.id).one()
        except SQLAlchemyError:
            db.session.rollback()

    def find_crew_member_by_name(self, full_name):
        try:
            return CrewMember.query.filter(CrewMember.full_name == full_name).one()
        except NoResultFound:
            return None

    def add_user(self, username):
        user = User(username=username)

        try:
            db.session.add(user)
            db.session.commit()
            return User.query.filter(User.id == user.id).one()
        except SQLAlchemyError:
            db.session.rollback()

    def add_user_movie(self, user_id, movie_id):
        try:
            user_movie = MovieUserAssociation(movie_id=movie_id, user_id=user_id)
            db.session.add(user_movie)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

    def find_all_users(self):
        return User.query.all()

    def find_user_by_id(self, id):
        try:
            return User.query.filter(User.id == id).one()
        except NoResultFound:
            return None

    def find_user_movies(self, user_id):
        user = self.find_user_by_id(user_id)
        return user.movies if user else []

    def find_user_movie(self, user_id, movie_id):
        try:
            return MovieUserAssociation.query.filter(
                MovieUserAssociation.user_id == user_id, MovieUserAssociation.movie_id == movie_id
            ).one()
        except NoResultFound:
            return None

    def delete_user_movie(self, user_id, movie_id):
        try:
            user_movie = self.find_user_movie(user_id, movie_id)
            db.session.delete(user_movie)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def update_user_movie(self, user_id, movie_id, personal_rating):
        try:
            user_movie = self.find_user_movie(user_id, movie_id)

            if not user_movie:
                return False

            user_movie.personal_rating = personal_rating
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    def __create_movie_crew_member_association(self, crew_member_name, movie_id, member_type):
        crew_member = self.find_crew_member_by_name(crew_member_name)

        if crew_member:
            crew_member_id = crew_member.id
        else:
            new_crew_member = self.add_crew_member(crew_member_name)
            crew_member_id = new_crew_member.id

        return MovieCrewMemberAssociation(movie_id=movie_id,
                                          crew_member_id=crew_member_id,
                                          member_type=member_type)


repo = SQLiteRepository()
