from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def find_all_movies(self):
        pass

    @abstractmethod
    def find_movies_by_title(self, title):
        pass

    @abstractmethod
    def find_movies_like(self, title):
        pass

    @abstractmethod
    def has_movie(self, id):
        pass

    @abstractmethod
    def add_movie(self, title, release_year, rating, poster_url, imdb_id):
        pass

    @abstractmethod
    def add_genre(self, name):
        pass

    @abstractmethod
    def add_crew_member(self, full_name):
        pass

    @abstractmethod
    def find_all_users(self):
        pass

    @abstractmethod
    def find_user_movies(self):
        pass

    @abstractmethod
    def delete_user_movie(self, id):
        pass

    @abstractmethod
    def update_user_movie(self, id, personal_rating):
        pass
