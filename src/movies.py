from repository.json_repository import JsonRepository
import crud_commands as crud_cmd
import commands as cmd
import menu


def main():
    """Initializes the movie repository and runs the main menu."""
    repo = JsonRepository("movies.json")
    repo.initialize()

    menu.add_command("Exit", cmd.exit_program)
    menu.add_command("List movies", lambda: crud_cmd.list_movies(repo))
    menu.add_command("Add movie", lambda: crud_cmd.add_movie(repo))
    menu.add_command("Update movie", lambda: crud_cmd.update_movie(repo))
    menu.add_command("Delete movie", lambda: crud_cmd.delete_movie(repo))
    menu.add_command("Stats", lambda: cmd.stats(repo))
    menu.add_command("Random movie", lambda: cmd.random_movie(repo))
    menu.add_command("Search movie", lambda: cmd.search_movie(repo))
    menu.add_command("Movies sorted by rating", lambda: cmd.sorted_by_rating(repo))
    menu.add_command("Movies sorted by year", lambda: cmd.sorted_by_year(repo))
    menu.add_command("Filter movies", lambda: cmd.filter_movies(repo))

    menu.run()


if __name__ == "__main__":
    main()
