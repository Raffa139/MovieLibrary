import repository as repo
import crud_commands as crud_cmd
import commands as cmd
import menu


def main():
    repo.initialize()

    menu.add_command("List movies", crud_cmd.list_movies)
    menu.add_command("Add movie", crud_cmd.add_movie)
    menu.add_command("Update movie", crud_cmd.update_movie)
    menu.add_command("Delete movie", crud_cmd.delete_movie)
    menu.add_command("Stats", cmd.stats)
    menu.add_command("Random movie", cmd.random_movie)
    menu.add_command("Search movie", cmd.search_movie)

    menu.run()


if __name__ == "__main__":
    main()
