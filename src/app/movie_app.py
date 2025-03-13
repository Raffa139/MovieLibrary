import app.crud_commands as crud_cmd
import app.commands as cmd
from menu.menu import Menu
from repository.irepository import IRepository
from omdb.omdb_client import OmdbClient


class MovieApp:
    """
    A class that represents the main application for managing movies.
    """

    def __init__(self, repo, omdb_client):
        """
        Initializes a MovieApp object.

        Args:
            repo (IRepository): The movie repository object.
            omdb_client (OmdbClient): The OMDB client object.
        """
        self._repo = repo
        self._omdb_client = omdb_client

    def start(self):
        """
        Starts the movie application, initializing the repository and running the main menu.
        """
        self._repo.initialize()

        menu = Menu("My Movies Database")
        menu.add_command("Exit", cmd.exit_program)
        menu.add_command("List movies", lambda: crud_cmd.list_movies(self._repo))
        menu.add_command("Add movie", lambda: crud_cmd.add_movie(self._repo, self._omdb_client))
        menu.add_command("Update movie", lambda: crud_cmd.update_movie(self._repo))
        menu.add_command("Delete movie", lambda: crud_cmd.delete_movie(self._repo))
        menu.add_command("Stats", lambda: cmd.stats(self._repo))
        menu.add_command("Random movie", lambda: cmd.random_movie(self._repo))
        menu.add_command("Search movie", lambda: cmd.search_movie(self._repo))
        menu.add_command("Movies sorted by rating", lambda: cmd.sorted_by_rating(self._repo))
        menu.add_command("Movies sorted by year", lambda: cmd.sorted_by_year(self._repo))
        menu.add_command("Filter movies", lambda: cmd.filter_movies(self._repo))
        menu.add_command("Generate website", lambda: cmd.generate_website(self._repo))

        menu.run()
