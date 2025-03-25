from .irepository import IRepository


class SQLiteRepository(IRepository):
    def find_all_movies(self):
        pass

    def find_movie_by_title(self, title):
        pass

    def has_movie(self, id):
        pass

    def add_movie(self, title, release_year, rating, poster_url, imdb_id):
        pass

    def add_genre(self, name):
        pass

    def add_crew_member(self, full_name):
        pass

    def find_all_users(self):
        pass

    def find_user_movies(self):
        pass

    def delete_user_movie(self, id):
        pass

    def update_user_movie(self, id, personal_rating):
        pass
