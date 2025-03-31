from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def find_all_movies(self):
        pass

    @abstractmethod
    def find_movie_by_id(self, id):
        pass

    @abstractmethod
    def find_movie_by_title(self, title):
        pass

    @abstractmethod
    def find_movies_like(self, title, limit=None):
        pass

    @abstractmethod
    def has_movie(self, *, id=None, title=None):
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def add_genre(self, name):
        pass

    @abstractmethod
    def find_genre_by_name(self, name):
        pass

    @abstractmethod
    def add_crew_member(self, full_name):
        pass

    @abstractmethod
    def find_crew_member_by_name(self, full_name):
        pass

    @abstractmethod
    def add_user(self, username, profile_picture_filename):
        pass

    @abstractmethod
    def add_user_movie(self, user_id, movie_id):
        pass

    @abstractmethod
    def find_all_users(self):
        pass

    @abstractmethod
    def find_user_by_id(self, id):
        pass

    @abstractmethod
    def has_user(self, id):
        pass

    @abstractmethod
    def find_user_movie(self, user_id, movie_id):
        pass

    @abstractmethod
    def has_user_movie(self, user_id, movie_id):
        pass

    @abstractmethod
    def delete_user_movie(self, user_id, movie_id):
        pass

    @abstractmethod
    def update_user_movie(self, user_id, movie_id, personal_rating):
        pass
