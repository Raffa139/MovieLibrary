commands = []


def print_title():
    """
    Prints the menu title.
    """
    print("********** My Movies Database **********")


def print_menu():
    """
    Prints the menu options.
    """
    print("\nMenu:")

    for i, command in enumerate(commands):
        print(f"{i}. {command['title']}")


def add_command(title, action):
    """
    Adds a command to the menu.

    Args:
        title (str): The title of the command.
        action (function): The function to execute when the command is selected.
    """
    commands.append({
        "title": title,
        "action": action
    })


def get_command():
    """
    Gets the user's command choice.

    Returns:
        int: The index of the selected command.
    """
    max_command_index = len(commands) - 1

    while True:
        print_menu()

        command = input(f"\nEnter choice (0-{max_command_index}): ").strip()

        try:
            command_index = int(command)

            if command_index < 0 or command_index > max_command_index:
                raise ValueError()

            return command_index
        except ValueError:
            print(f"Invalid choice '{command}'")


def run_command(command_index):
    """
    Executes the selected command.

    Args:
        command_index (int): The index of the command to execute.
    """
    print()
    commands[command_index]["action"]()
    input("\nPress enter to continue ")


def run():
    """
    Runs the menu, displaying the title and handling user input.
    """
    print_title()

    while True:
        command = get_command()
        run_command(command)
