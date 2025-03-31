import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main.repository import Base
from main.repository.sqlite_repository import SQLiteRepository

TEST_DB_URI = "sqlite:///:memory:"

engine = create_engine(TEST_DB_URI)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.create_all(engine)
    session_ = Session()

    try:
        yield session_
    finally:
        session_.rollback()
        session_.close()
        Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def repo(session):
    return SQLiteRepository(session=session)


class TestSQLiteRepository:
    def test_find_all_movies_empty(self, repo):
        assert repo.find_all_movies() == []

    def test_add_and_find_movie_by_id(self, repo):
        movie_data = {
            "title": "Test Movie",
            "release_year": 2023,
            "rating": 8.5,
            "poster_url": "test_url",
            "imdb_id": "tt1234567",
            "genre_names": ["Action", "Comedy"],
            "directors": ["Director One"],
            "writers": ["Writer One"],
            "actors": ["Actor One"]
        }
        added_movie = repo.add_movie(**movie_data)
        found_movie = repo.find_movie_by_id(added_movie.id)
        assert found_movie is not None
        assert found_movie.title == "Test Movie"
        assert len(found_movie.genres) == 2
        assert any(g.name == "Action" for g in found_movie.genres)
        assert any(g.name == "Comedy" for g in found_movie.genres)
        assert any(
            mcm.crew_member.full_name == "Director One" and mcm.member_type == "director" for mcm in
            found_movie.crew_members)
        assert any(
            mcm.crew_member.full_name == "Writer One" and mcm.member_type == "writer" for mcm in
            found_movie.crew_members)
        assert any(
            mcm.crew_member.full_name == "Actor One" and mcm.member_type == "actor" for mcm in
            found_movie.crew_members)

    def test_find_movie_by_id_not_found(self, repo):
        assert repo.find_movie_by_id(999) is None

    def test_add_and_find_movie_by_title(self, repo):
        movie_data = {
            "title": "Another Test Movie",
            "release_year": 2024,
            "rating": 7.9,
            "poster_url": "another_url",
            "imdb_id": "tt9876543",
            "genre_names": ["Drama"],
            "directors": [],
            "writers": [],
            "actors": []
        }
        added_movie = repo.add_movie(**movie_data)
        found_movie = repo.find_movie_by_title("Another Test Movie")
        assert found_movie is not None
        assert found_movie.id == added_movie.id

    def test_find_movie_by_title_not_found(self, repo):
        assert repo.find_movie_by_title("Nonexistent Movie") is None

    def test_find_movies_like(self, repo):
        repo.add_movie(title="Movie One", release_year=2020, rating=7.0, poster_url="", imdb_id="",
                       genre_names=[], directors=[], writers=[], actors=[])
        repo.add_movie(title="Movie Two", release_year=2021, rating=7.5, poster_url="", imdb_id="",
                       genre_names=[], directors=[], writers=[], actors=[])
        repo.add_movie(title="Some Other Film", release_year=2022, rating=8.0, poster_url="",
                       imdb_id="", genre_names=[], directors=[], writers=[], actors=[])
        found_movies = repo.find_movies_like("Movie")
        assert len(found_movies) == 2
        assert any(movie.title == "Movie One" for movie in found_movies)
        assert any(movie.title == "Movie Two" for movie in found_movies)

    def test_find_movies_like_case_insensitive(self, repo):
        repo.add_movie(title="The Movie", release_year=2023, rating=8.2, poster_url="", imdb_id="",
                       genre_names=[], directors=[], writers=[], actors=[])
        found_movies = repo.find_movies_like("the movie")
        assert len(found_movies) == 1
        assert found_movies[0].title == "The Movie"

    def test_find_movies_like_limit(self, repo):
        repo.add_movie(title="Movie A", release_year=2020, rating=6.5, poster_url="", imdb_id="",
                       genre_names=[], directors=[], writers=[], actors=[])
        repo.add_movie(title="Movie B", release_year=2021, rating=7.1, poster_url="", imdb_id="",
                       genre_names=[], directors=[], writers=[], actors=[])
        repo.add_movie(title="Movie C", release_year=2022, rating=7.8, poster_url="", imdb_id="",
                       genre_names=[], directors=[], writers=[], actors=[])
        found_movies = repo.find_movies_like("Movie", limit=2)
        assert len(found_movies) == 2
        assert any(movie.title == "Movie A" for movie in found_movies)
        assert any(movie.title == "Movie B" for movie in found_movies)
        assert not any(movie.title == "Movie C" for movie in found_movies)

    def test_has_movie_by_id_exists(self, repo):
        movie_data = {"title": "Has Movie ID", "release_year": 2023, "rating": 0.0,
                      "poster_url": "", "imdb_id": "", "genre_names": [], "directors": [],
                      "writers": [], "actors": []}
        added_movie = repo.add_movie(**movie_data)
        assert repo.has_movie(id=added_movie.id) is True

    def test_has_movie_by_id_not_exists(self, repo):
        assert repo.has_movie(id=999) is False

    def test_has_movie_by_title_exists(self, repo):
        movie_data = {"title": "Has Movie Title", "release_year": 2023, "rating": 0.0,
                      "poster_url": "", "imdb_id": "", "genre_names": [], "directors": [],
                      "writers": [], "actors": []}
        repo.add_movie(**movie_data)
        assert repo.has_movie(title="Has Movie Title") is True

    def test_has_movie_by_title_not_exists(self, repo):
        assert repo.has_movie(title="Nonexistent Title") is False

    def test_add_movie_new_genres_and_crew(self, repo):
        movie_data = {
            "title": "New Elements Movie",
            "release_year": 2025,
            "rating": 9.0,
            "poster_url": "new_url",
            "imdb_id": "tt0000001",
            "genre_names": ["Sci-Fi", "Thriller"],
            "directors": ["Greta Gerwig"],
            "writers": ["Noah Baumbach", "Greta Gerwig"],
            "actors": ["Margot Robbie", "Ryan Gosling"]
        }
        added_movie = repo.add_movie(**movie_data)
        assert len(added_movie.genres) == 2
        assert any(g.name == "Sci-Fi" for g in added_movie.genres)
        assert any(g.name == "Thriller" for g in added_movie.genres)
        assert len(added_movie.crew_members) == 5
        assert (sum(1 for mcm in added_movie.crew_members if
                    mcm.member_type == "director" and mcm.crew_member.full_name == "Greta Gerwig")
                == 1)
        assert (sum(1 for mcm in added_movie.crew_members if
                    mcm.member_type == "writer" and mcm.crew_member.full_name == "Noah Baumbach")
                == 1)
        assert sum(1 for mcm in added_movie.crew_members if
                   mcm.member_type == "writer" and mcm.crew_member.full_name == "Greta Gerwig") == 1
        assert sum(1 for mcm in added_movie.crew_members if
                   mcm.member_type == "actor" and mcm.crew_member.full_name == "Margot Robbie") == 1
        assert sum(1 for mcm in added_movie.crew_members if
                   mcm.member_type == "actor" and mcm.crew_member.full_name == "Ryan Gosling") == 1

    def test_add_movie_existing_genre_and_crew(self, repo):
        repo.add_genre("Action")
        repo.add_crew_member("Existing Director")
        movie_data = {
            "title": "Existing Elements Movie",
            "release_year": 2026,
            "rating": 8.8,
            "poster_url": "existing_url",
            "imdb_id": "tt0000002",
            "genre_names": ["Action"],
            "directors": ["Existing Director"],
            "writers": [],
            "actors": []
        }
        added_movie = repo.add_movie(**movie_data)
        assert len(added_movie.genres) == 1
        assert added_movie.genres[0].name == "Action"
        assert len(added_movie.crew_members) == 1
        assert added_movie.crew_members[0].member_type == "director"
        assert added_movie.crew_members[0].crew_member.full_name == "Existing Director"

    def test_add_genre_and_find_by_name(self, repo):
        added_genre = repo.add_genre("Fantasy")
        found_genre = repo.find_genre_by_name("Fantasy")
        assert found_genre is not None
        assert found_genre.id == added_genre.id
        assert found_genre.name == "Fantasy"

    def test_find_genre_by_name_not_found(self, repo):
        assert repo.find_genre_by_name("Nonexistent Genre") is None

    def test_add_crew_member_and_find_by_name(self, repo):
        added_crew_member = repo.add_crew_member("Keanu Reeves")
        found_crew_member = repo.find_crew_member_by_name("Keanu Reeves")
        assert found_crew_member is not None
        assert found_crew_member.id == added_crew_member.id
        assert found_crew_member.full_name == "Keanu Reeves"

    def test_find_crew_member_by_name_not_found(self, repo):
        assert repo.find_crew_member_by_name("Nonexistent Actor") is None

    def test_add_user_and_find_by_id(self, repo):
        added_user = repo.add_user("testuser", "profile.jpg")
        found_user = repo.find_user_by_id(added_user.id)
        assert found_user is not None
        assert found_user.id == added_user.id
        assert found_user.username == "testuser"
        assert found_user.profile_picture == "profile.jpg"

    def test_find_user_by_id_not_found(self, repo):
        assert repo.find_user_by_id(1) is None

    def test_find_all_users_empty(self, repo):
        assert repo.find_all_users() == []

    def test_add_user_movie(self, repo):
        user = repo.add_user("user1", "pic1.png")
        movie = repo.add_movie(title="User Movie", release_year=2023, rating=0.0, poster_url="",
                               imdb_id="", genre_names=[], directors=[], writers=[], actors=[])
        repo.add_user_movie(user.id, movie.id)
        user_movie = repo.find_user_movie(user.id, movie.id)
        assert user_movie is not None
        assert user_movie.user_id == user.id
        assert user_movie.movie_id == movie.id

    def test_find_user_movie_not_found(self, repo):
        assert repo.find_user_movie(1, 1) is None

    def test_has_user_movie_exists(self, repo):
        user = repo.add_user("user_has", "pic.png")
        movie = repo.add_movie(title="Has User Movie", release_year=2023, rating=0.0, poster_url="",
                               imdb_id="", genre_names=[], directors=[], writers=[], actors=[])
        repo.add_user_movie(user.id, movie.id)
        assert repo.has_user_movie(user.id, movie.id) is True

    def test_has_user_movie_not_exists(self, repo):
        assert repo.has_user_movie(1, 1) is False

    def test_delete_user_movie_success(self, repo):
        user = repo.add_user("user_del", "del.png")
        movie = repo.add_movie(title="Delete User Movie", release_year=2023, rating=0.0,
                               poster_url="", imdb_id="", genre_names=[], directors=[], writers=[],
                               actors=[])
        repo.add_user_movie(user.id, movie.id)
        assert repo.has_user_movie(user.id, movie.id) is True
        assert repo.delete_user_movie(user.id, movie.id) is True
        assert repo.has_user_movie(user.id, movie.id) is False

    def test_delete_user_movie_not_found(self, repo):
        assert repo.delete_user_movie(1, 1) is False

    def test_update_user_movie_success(self, repo):
        user = repo.add_user("user_upd", "upd.png")
        movie = repo.add_movie(title="Update User Movie", release_year=2023, rating=0.0,
                               poster_url="", imdb_id="", genre_names=[], directors=[], writers=[],
                               actors=[])
        repo.add_user_movie(user.id, movie.id)
        assert repo.update_user_movie(user.id, movie.id, 9.5) is True
        updated_user_movie = repo.find_user_movie(user.id, movie.id)
        assert updated_user_movie.personal_rating == 9.5

    def test_update_user_movie_not_found(self, repo):
        assert repo.update_user_movie(1, 1, 10.0) is False

    def test_has_user_exists(self, repo):
        user = repo.add_user("user_exists", "exists.png")
        assert repo.has_user(user.id) is True

    def test_has_user_not_exists(self, repo):
        assert repo.has_user(99) is False
