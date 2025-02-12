commands = []


def print_title():
    print("********** My Movies Database **********")


def print_menu():
    print("\nMenu:")

    for i, command in enumerate(commands):
        print(f"{i}. {command['title']}")


def add_command(title, action):
    commands.append({
        "title": title,
        "action": action
    })


def get_command():
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
    print()
    commands[command_index]["action"]()
    input("\nPress enter to continue ")


def run():
    print_title()

    while True:
        command = get_command()
        run_command(command)
