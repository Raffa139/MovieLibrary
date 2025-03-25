from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db


class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    imdb_id = Column(String)
    title = Column(String)
    release_year = Column(Integer)
    rating = Column(Float)
    poster_url = Column(String)
    genres = relationship("Genre", secondary="movie_genre")
    crew_members = relationship("MovieCrewMemberAssociation")


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    movie_associations = relationship("MovieUserAssociation")
    movies = relationship("Movie", secondary="movie_user")


class Genre(db.Model):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class CrewMember(db.Model):
    __tablename__ = "crew_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)


class MovieUserAssociation(db.Model):
    __tablename__ = "movie_user"

    movie_id = Column(Integer, ForeignKey(Movie.id), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    personal_rating = Column(Float)

    def __repr__(self):
        return (f"<MovieUserAssociation movie_id={self.movie_id}, user_id={self.user_id}, "
                f"personal_rating={self.personal_rating}>")


class MovieCrewMemberAssociation(db.Model):
    __tablename__ = "movie_crew_member"

    movie_id = Column(Integer, ForeignKey(Movie.id), primary_key=True)
    crew_member_id = Column(Integer, ForeignKey(CrewMember.id), primary_key=True)
    member_type = Column(String, primary_key=True)

    def __repr__(self):
        return (f"<MovieCrewMemberAssociation movie_id={self.movie_id}, crew_member_id="
                f"{self.crew_member_id}, member_type={self.member_type}>")


class MovieGenreAssociation(db.Model):
    __tablename__ = "movie_genre"

    movie_id = Column(Integer, ForeignKey(Movie.id), primary_key=True)
    genre_id = Column(Integer, ForeignKey(Genre.id), primary_key=True)

    def __repr__(self):
        return f"<MovieGenreAssociation movie_id={self.movie_id}, genre_id={self.genre_id}>"
