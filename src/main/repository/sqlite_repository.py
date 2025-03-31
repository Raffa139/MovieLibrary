from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from .irepository import IRepository
from .entities import Movie, Genre, CrewMember, User, MovieCrewMemberAssociation, \
    MovieUserAssociation
from . import db


class SQLiteRepository(IRepository):
    def __init__(self, *, session):
        self._session = session

    def find_all_movies(self):
        query = select(Movie)
        return self._exec_query(query).scalars().all()

    def find_movie_by_id(self, id):
        try:
            query = select(Movie).where(Movie.id == id)
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def find_movie_by_title(self, title):
        try:
            query = select(Movie).where(Movie.title == title)
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def find_movies_like(self, title, limit=None):
        query = select(Movie).where(Movie.title.ilike(f"%{title}%"))

        if limit:
            query = query.limit(limit)

        return self._exec_query(query).scalars().all()

    def has_movie(self, *, id=None, title=None):
        if id:
            return self.find_movie_by_id(id) is not None

        if title:
            return self.find_movie_by_title(title) is not None

        return False

    def add_movie(
            self,
            title,
            release_year,
            rating,
            poster_url,
            imdb_id,
            genre_names,
            directors,
            writers,
            actors
    ):
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

            self._session.add(movie)
            self._session.flush()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e

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
            self._session.add_all(director_associations)
            self._session.add_all(writer_associations)
            self._session.add_all(actor_associations)
            self._session.commit()
            return self._exec_query(select(Movie).where(Movie.id == movie.id)).scalar_one()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e

    def add_genre(self, name):
        genre = Genre(name=name)

        try:
            self._session.add(genre)
            self._session.commit()
            return self._exec_query(select(Genre).where(Genre.id == genre.id)).scalar_one()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e

    def find_genre_by_name(self, name):
        try:
            query = select(Genre).where(Genre.name == name)
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def add_crew_member(self, full_name):
        crew_member = CrewMember(full_name=full_name)

        try:
            self._session.add(crew_member)
            self._session.commit()
            return self._exec_query(
                select(CrewMember).where(CrewMember.id == crew_member.id)
            ).scalar_one()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e

    def find_crew_member_by_name(self, full_name):
        try:
            query = select(CrewMember).where(CrewMember.full_name == full_name)
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def add_user(self, username, profile_picture_file_name):
        user = User(username=username, profile_picture=profile_picture_file_name)

        try:
            self._session.add(user)
            self._session.commit()
            return self._exec_query(select(User).where(User.id == user.id)).scalar_one()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e

    def add_user_movie(self, user_id, movie_id):
        try:
            user_movie = MovieUserAssociation(movie_id=movie_id, user_id=user_id)
            self._session.add(user_movie)
            self._session.commit()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e

    def find_all_users(self):
        query = select(User)
        return self._exec_query(query).scalars().all()

    def find_user_by_id(self, id):
        try:
            query = select(User).where(User.id == id)
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def has_user(self, id):
        return self.find_user_by_id(id) is not None

    def find_user_movie(self, user_id, movie_id):
        try:
            query = select(MovieUserAssociation).where(
                MovieUserAssociation.user_id == user_id, MovieUserAssociation.movie_id == movie_id
            )
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def has_user_movie(self, user_id, movie_id):
        return self.find_user_movie(user_id, movie_id) is not None

    def delete_user_movie(self, user_id, movie_id):
        try:
            user_movie = self.find_user_movie(user_id, movie_id)
            self._session.delete(user_movie)
            self._session.commit()
            return True
        except SQLAlchemyError:
            self._session.rollback()
            return False

    def update_user_movie(self, user_id, movie_id, personal_rating):
        try:
            user_movie = self.find_user_movie(user_id, movie_id)

            if not user_movie:
                return False

            user_movie.personal_rating = personal_rating
            self._session.commit()
            return True
        except SQLAlchemyError:
            self._session.rollback()
            return False

    def _exec_query(self, query):
        return self._session.execute(query)

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


repo = SQLiteRepository(session=db.session)
