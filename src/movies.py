import repository as repo
import crud_commands as crud_cmd
import commands as cmd
import menu


def main():
    """Initializes the movie repository and runs the main menu."""
    repo.initialize()

    menu.add_command("Exit", cmd.exit_program)
    menu.add_command("List movies", crud_cmd.list_movies)
    menu.add_command("Add movie", crud_cmd.add_movie)
    menu.add_command("Update movie", crud_cmd.update_movie)
    menu.add_command("Delete movie", crud_cmd.delete_movie)
    menu.add_command("Stats", cmd.stats)
    menu.add_command("Random movie", cmd.random_movie)
    menu.add_command("Search movie", cmd.search_movie)
    menu.add_command("Movies sorted by rating", cmd.sorted_by_rating)
    menu.add_command("Movies sorted by year", cmd.sorted_by_year)
    menu.add_command("Filter movies", cmd.filter_movies)

    menu.run()


if __name__ == "__main__":
    main()
