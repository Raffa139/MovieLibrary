class Menu:
    """
    A class representing a text-based menu.
    """

    def __init__(self, title):
        """
        Initializes a Menu object.

        Args:
            title (str): The title of the menu.
        """
        self.title = title
        self.commands = []

    def print_title(self):
        """
        Prints the menu title.
        """
        print(f"********** {self.title} **********")

    def print_menu(self):
        """
        Prints the menu options.
        """
        print("\n   Menu")
        print("   ----")

        for i, command in enumerate(self.commands):
            print(f"{i + 1}. {command['title']}")

    def add_command(self, title, action):
        """
        Adds a command to the menu.

        Args:
            title (str): The title of the command.
            action (function): The function to execute when the command is selected.
        """
        self.commands.append({
            "title": title,
            "action": action
        })

    def get_command(self):
        """
        Gets the user's command choice.

        Returns:
            int: The index of the selected command.
        """
        max_command_index = len(self.commands) - 1

        while True:
            self.print_menu()

            command = input(f"\nEnter choice (1-{max_command_index + 1}): ").strip()

            try:
                command_index = int(command) - 1

                if command_index < 0 or command_index > max_command_index:
                    raise ValueError()

                return command_index
            except ValueError:
                print(f"Invalid choice '{command}'")

    def run_command(self, command_index):
        """
        Executes the selected command.

        Args:
            command_index (int): The index of the command to execute.
        """
        print()
        self.commands[command_index]["action"]()
        input("\nPress enter to continue ")

    def run(self):
        """
        Runs the menu, displaying the title and handling user input.
        """
        self.print_title()

        while True:
            command = self.get_command()
            self.run_command(command)
