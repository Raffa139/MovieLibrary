def input_str(prompt, error_message):
    while True:
        try:
            string = input(prompt)

            if not string:
                raise ValueError()

            return string
        except ValueError:
            print(error_message)


def input_int(prompt, error_message):
    while True:
        try:
            number = int(input(prompt))

            if number < 0:
                raise ValueError()

            return number
        except ValueError:
            print(error_message)


def input_float(prompt, error_message):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(error_message)
