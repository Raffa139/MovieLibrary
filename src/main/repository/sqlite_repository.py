from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from .irepository import IRepository
from .entities import Movie, Genre, CrewMember, User, MovieCrewMemberAssociation, \
    MovieUserAssociation
from . import db


class SQLiteRepository(IRepository):
    """A repository implementation using SQLite as the database."""

    def __init__(self, *, session):
        """
        Initializes the SQLiteRepository with a database session.

        Args:
            session (sqlalchemy.orm.Session): The SQLAlchemy session to use for database operations.
        """
        self._session = session

    def find_all_movies(self):
        """
        Finds all movies in the database.

        Returns:
            list[Movie]: A list of all Movie objects in the database.
        """
        query = select(Movie)
        return self._exec_query(query).scalars().all()

    def find_movie_by_id(self, id):
        """
        Finds a movie by its unique ID.

        Args:
            id (int): The ID of the movie to find.

        Returns:
            Movie or None: The Movie object with the given ID, or None if not found.
        """
        try:
            query = select(Movie).where(Movie.id == id)
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def find_movie_by_title(self, title):
        """
        Finds a movie by its title.

        Args:
            title (str): The title of the movie to find.

        Returns:
            Movie or None: The Movie object with the given title, or None if not found.
        """
        try:
            query = select(Movie).where(Movie.title == title)
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def find_movies_like(self, title, limit=None):
        """
        Finds movies whose title contains the given string (case-insensitive).

        Args:
            title (str): The substring to search for in movie titles.
            limit (int): The maximum number of movies to return. Defaults to None.

        Returns:
            list[Movie]: A list of Movie objects whose titles contain the search string.
        """
        query = select(Movie).where(Movie.title.ilike(f"%{title}%"))

        if limit:
            query = query.limit(limit)

        return self._exec_query(query).scalars().all()

    def has_movie(self, *, id=None, title=None):
        """
        Checks if a movie exists based on either its ID or title.

        Args:
            id (int): The ID of the movie to check for. Defaults to None.
            title (str): The title of the movie to check for. Defaults to None.

        Returns:
            bool: True if a movie with the given ID or title exists, False otherwise.
        """
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
        """
        Adds a new movie to the database, including its genres and crew members.

        Args:
            title (str): The title of the movie.
            release_year (int): The year the movie was released.
            rating (float): The rating of the movie.
            poster_url (str): The URL of the movie's poster.
            imdb_id (str): The IMDb ID of the movie.
            genre_names (list[str]): A list of genre names for the movie.
            directors (list[str]): A list of director names for the movie.
            writers (list[str]): A list of writer names for the movie.
            actors (list[str]): A list of actor names for the movie.

        Returns:
            Movie: The newly added Movie object.

        Raises:
            SQLAlchemyError: If any database error occurs during the operation.
        """
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
        """
        Adds a new genre to the database.

        Args:
            name (str): The name of the genre to add.

        Returns:
            Genre: The newly added Genre object.

        Raises:
            SQLAlchemyError: If any database error occurs during the operation.
        """
        genre = Genre(name=name)

        try:
            self._session.add(genre)
            self._session.commit()
            return self._exec_query(select(Genre).where(Genre.id == genre.id)).scalar_one()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e

    def find_genre_by_name(self, name):
        """
        Finds a genre by its name.

        Args:
            name (str): The name of the genre to find.

        Returns:
            Genre or None: The Genre object with the given name, or None if not found.
        """
        try:
            query = select(Genre).where(Genre.name == name)
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def add_crew_member(self, full_name):
        """
        Adds a new crew member to the database.

        Args:
            full_name (str): The full name of the crew member to add.

        Returns:
            CrewMember: The newly added CrewMember object.

        Raises:
            SQLAlchemyError: If any database error occurs during the operation.
        """
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
        """
        Finds a crew member by their full name.

        Args:
            full_name (str): The full name of the crew member to find.

        Returns:
            CrewMember or None: The CrewMember object with the given full name, or None if not
            found.
        """
        try:
            query = select(CrewMember).where(CrewMember.full_name == full_name)
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def add_user(self, username, profile_picture_filename):
        """
        Adds a new user to the database.

        Args:
            username (str): The username of the new user.
            profile_picture_filename (str): The filename of the user's profile picture.

        Returns:
            User: The newly added User object.

        Raises:
            SQLAlchemyError: If any database error occurs during the operation.
        """
        user = User(username=username, profile_picture=profile_picture_filename)

        try:
            self._session.add(user)
            self._session.commit()
            return self._exec_query(select(User).where(User.id == user.id)).scalar_one()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e

    def add_user_movie(self, user_id, movie_id):
        """
        Associates a user with a movie.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.

        Raises:
            SQLAlchemyError: If any database error occurs during the operation.
        """
        try:
            user_movie = MovieUserAssociation(movie_id=movie_id, user_id=user_id)
            self._session.add(user_movie)
            self._session.commit()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e

    def find_all_users(self):
        """
        Finds all users in the database.

        Returns:
            list[User]: A list of all User objects in the database.
        """
        query = select(User)
        return self._exec_query(query).scalars().all()

    def find_user_by_id(self, id):
        """
        Finds a user by their unique ID.

        Args:
            id (int): The ID of the user to find.

        Returns:
            User or None: The User object with the given ID, or None if not found.
        """
        try:
            query = select(User).where(User.id == id)
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def has_user(self, id):
        """
        Checks if a user with the given ID exists.

        Args:
            id (int): The ID of the user to check for.

        Returns:
            bool: True if a user with the given ID exists, False otherwise.
        """
        return self.find_user_by_id(id) is not None

    def find_user_movie(self, user_id, movie_id):
        """
        Finds the association between a user and a movie.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.

        Returns:
            MovieUserAssociation or None: The MovieUserAssociation object for the given user and
            movie, or None if not found.
        """
        try:
            query = select(MovieUserAssociation).where(
                MovieUserAssociation.user_id == user_id, MovieUserAssociation.movie_id == movie_id
            )
            return self._exec_query(query).scalar_one()
        except NoResultFound:
            return None

    def has_user_movie(self, user_id, movie_id):
        """
        Checks if a user is associated with a movie.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.

        Returns:
            bool: True if the user is associated with the movie, False otherwise.
        """
        return self.find_user_movie(user_id, movie_id) is not None

    def delete_user_movie(self, user_id, movie_id):
        """
        Deletes the association between a user and a movie.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.

        Returns:
            bool: True if the association was successfully deleted, False otherwise.
        """
        try:
            user_movie = self.find_user_movie(user_id, movie_id)
            self._session.delete(user_movie)
            self._session.commit()
            return True
        except SQLAlchemyError:
            self._session.rollback()
            return False

    def update_user_movie(self, user_id, movie_id, personal_rating):
        """
        Updates the personal rating of a movie for a specific user.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            personal_rating (int): The personal rating given by the user to the movie.

        Returns:
            bool: True if the personal rating was successfully updated, False otherwise.
        """
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
        """
        Executes a SQLAlchemy query.

        Args:
            query (sqlalchemy.sql.selectable.Select): The SQLAlchemy select query to execute.

        Returns:
            sqlalchemy.engine.cursor.CursorResult: The result of the executed query.
        """
        return self._session.execute(query)

    def __create_movie_crew_member_association(self, crew_member_name, movie_id, member_type):
        """
        Creates an association between a movie and a crew member.

        Args:
            crew_member_name (str): The full name of the crew member.
            movie_id (int): The ID of the movie.
            member_type (str): The type of crew member (e.g., "director", "writer", "actor").

        Returns:
            MovieCrewMemberAssociation: The newly created association object.
        """
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
