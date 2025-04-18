from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db


class Movie(db.Model):
    """Represents a movie in the database."""
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    imdb_id = Column(String)
    title = Column(String)
    release_year = Column(Integer)
    rating = Column(Float)
    poster_url = Column(String)
    genres = relationship("Genre", secondary="movie_genre")
    crew_members = relationship("MovieCrewMemberAssociation")

    def to_dict(self):
        """Returns a dictionary representation of the movie."""
        return {
            "id": self.id,
            "imdb_id": self.imdb_id,
            "title": self.title,
            "release_year": self.release_year,
            "rating": self.rating,
            "poster_url": self.poster_url,
            "genres": [genre.to_dict() for genre in self.genres]
        }


class User(db.Model):
    """Represents a user in the database."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    profile_picture = Column(String)
    movie_associations = relationship("MovieUserAssociation")
    movies = relationship("Movie", secondary="movie_user")

    def to_dict(self):
        """Returns a dictionary representation of the user."""
        return {
            "id": self.id,
            "username": self.username,
            "movies": [movie.to_dict() for movie in self.movies]
        }


class Genre(db.Model):
    """Represents a movie genre in the database."""
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def to_dict(self):
        """Returns a dictionary representation of the genre."""
        return {
            "id": self.id,
            "name": self.name,
        }


class CrewMember(db.Model):
    """Represents a crew member (director, writer, actor) in the database."""
    __tablename__ = "crew_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)

    def to_dict(self):
        """Returns a dictionary representation of the crew member."""
        return {
            "id": self.id,
            "full_name": self.full_name,
        }


class MovieUserAssociation(db.Model):
    """
    Represents the association between a movie and a user, including the user's personal rating.
    """
    __tablename__ = "movie_user"

    movie_id = Column(Integer, ForeignKey(Movie.id), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    movie = relationship("Movie", foreign_keys="MovieUserAssociation.movie_id")
    personal_rating = Column(Float)

    def __repr__(self):
        """Returns a string representation of the MovieUserAssociation object."""
        return (f"<MovieUserAssociation movie_id={self.movie_id}, user_id={self.user_id}, "
                f"personal_rating={self.personal_rating}>")


class MovieCrewMemberAssociation(db.Model):
    """
    Represents the association between a movie and a crew member, including the crew member's role.
    """
    __tablename__ = "movie_crew_member"

    movie_id = Column(Integer, ForeignKey(Movie.id), primary_key=True)
    crew_member_id = Column(Integer, ForeignKey(CrewMember.id), primary_key=True)
    crew_member = relationship("CrewMember",
                               foreign_keys="MovieCrewMemberAssociation.crew_member_id")
    member_type = Column(String, primary_key=True)

    def __repr__(self):
        """Returns a string representation of the MovieCrewMemberAssociation object."""
        return (f"<MovieCrewMemberAssociation movie_id={self.movie_id}, crew_member_id="
                f"{self.crew_member_id}, member_type={self.member_type}>")


class MovieGenreAssociation(db.Model):
    """Represents the association between a movie and a genre."""
    __tablename__ = "movie_genre"

    movie_id = Column(Integer, ForeignKey(Movie.id), primary_key=True)
    genre_id = Column(Integer, ForeignKey(Genre.id), primary_key=True)

    def __repr__(self):
        """Returns a string representation of the MovieGenreAssociation object."""
        return f"<MovieGenreAssociation movie_id={self.movie_id}, genre_id={self.genre_id}>"
