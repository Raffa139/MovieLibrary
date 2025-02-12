def input_str(prompt, *, error_message):
    while True:
        try:
            user_input = input(prompt)

            if not user_input:
                raise ValueError()

            return user_input
        except ValueError:
            print(error_message)


def input_yes_no(prompt):
    while True:
        try:
            user_input = input(f"{prompt} (Y/N): ").lower()

            if user_input == "y" or user_input == "n":
                return user_input == "y"

            raise ValueError()
        except ValueError:
            print("Please enter 'Y' or 'N'")


def input_int(prompt, *, error_message):
    while True:
        try:
            number = int(input(prompt))

            if number < 0:
                raise ValueError()

            return number
        except ValueError:
            print(error_message)


def input_optional_int(prompt, *, error_message):
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
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(error_message)


def input_optional_float(prompt, *, error_message):
    while True:
        try:
            user_input = input(prompt)

            if not user_input:
                return None

            return float(user_input)
        except ValueError:
            print(error_message)
