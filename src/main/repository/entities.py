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
    # genres = relationship("Genre")
    # crew_members = relationship("CrewMember")


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    # movies = relationship("Movie")


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


class MovieCrewMemberAssociation(db.Model):
    __tablename__ = "movie_crew_member"

    movie_id = Column(Integer, ForeignKey(Movie.id), primary_key=True)
    crew_member_id = Column(Integer, ForeignKey(CrewMember.id), primary_key=True)
    member_type = Column(String, primary_key=True)


class MovieGenreAssociation(db.Model):
    __tablename__ = "movie_genre"

    movie_id = Column(Integer, ForeignKey(Movie.id), primary_key=True)
    genre_id = Column(Integer, ForeignKey(Genre.id), primary_key=True)
