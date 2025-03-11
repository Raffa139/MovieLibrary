def input_str(prompt, *, error_message):
    """
    Prompts the user for a string input and validates that it is not empty.

    Args:
        prompt (str): The prompt message to display to the user.
        error_message (str): The error message to display if the input is invalid.

    Returns:
        str: The user's input string.
    """
    while True:
        try:
            user_input = input(prompt)

            if not user_input:
                raise ValueError()

            return user_input
        except ValueError:
            print(error_message)


def input_yes_no(prompt):
    """
    Prompts the user for a yes/no input.

    Args:
        prompt (str): The prompt message to display to the user.

    Returns:
        bool: True if the user enters 'Y', False if the user enters 'N'.
    """
    while True:
        try:
            user_input = input(f"{prompt} (Y/N): ").lower()

            if user_input in ("y", "n"):
                return user_input == "y"

            raise ValueError()
        except ValueError:
            print("Please enter 'Y' or 'N'")


def input_int(prompt, *, error_message):
    """
    Prompts the user for an integer input and validates that it is non-negative.

    Args:
        prompt (str): The prompt message to display to the user.
        error_message (str): The error message to display if the input is invalid.

    Returns:
        int: The user's input integer.
    """
    while True:
        try:
            number = int(input(prompt))

            if number < 0:
                raise ValueError()

            return number
        except ValueError:
            print(error_message)


def input_optional_int(prompt, *, error_message):
    """
    Prompts the user for an optional integer input and validates that it is non-negative.

    Args:
        prompt (str): The prompt message to display to the user.
        error_message (str): The error message to display if the input is invalid.

    Returns:
        int or None: The user's input integer, or None if the user enters an empty string.
    """
    while True:
        try:
            user_input = input(prompt)

            if not user_input:
                return None

            number = int(user_input)

            if number < 0:
                raise ValueError()

            return number
        except ValueError:
            print(error_message)


def input_float(prompt, *, error_message):
    """
    Prompts the user for a float input.

    Args:
        prompt (str): The prompt message to display to the user.
        error_message (str): The error message to display if the input is invalid.

    Returns:
        float: The user's input float.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(error_message)


def input_optional_float(prompt, *, error_message):
    """
    Prompts the user for an optional float input.

    Args:
        prompt (str): The prompt message to display to the user.
        error_message (str): The error message to display if the input is invalid.

    Returns:
        float or None: The user's input float, or None if the user enters an empty string.
    """
    while True:
        try:
            user_input = input(prompt)

            if not user_input:
                return None

            return float(user_input)
        except ValueError:
            print(error_message)
