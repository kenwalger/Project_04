import re


# Clears the screen
def clear_screen():
    """Clears the screen"""
    print("\033c", end="")


# Test valid datetime
def is_valid_date(text):
    return (re.match(r'\d{4}-\d{2}-\d{2}', str(text)) and
            0 < int(str(text)[5:7]) < 13 and
            0 < int(str(text)[8:10]) < 32)


# Clears the screen and displays the headline
def header_line(text):
    """Clears the screen and displays the headline"""
    if len(text) > 0:
        clear_screen()
        print(text)
        print("=" * len(text) + "\n")


# Displays message if exists
def display_message(message):
    """Displays error messages with a newline at the end for readability"""
    if message.strip() != "":
        print(message + "\n")


# Display a user menu
def menu(title, *args):
    """Creates the user menu and takes and checks input"""
    message = ""
    while True:
        # Clear screen
        header_line(title)

        # Display menu options
        item = 1
        for arg in args:
            print("{}. {}".format(item, arg))
            item += 1

        print("")

        # Display any messages
        display_message(message)

        # Display input line
        menu_select = input("1-{} : ".format(str(item - 1)))

        # Check the enty is numeric and in the correct range provided
        if (not menu_select.isnumeric() or
                int(menu_select) not in range(1, item)):
            message = ("Sorry, your entry was not valid. Please select from "
                       "options provided.")
            continue

        return menu_select


def edit(title, header_text="", type="text", required=True, value=""):
    """Handles user input"""
    message = ""
    while True:
        header_line(header_text)
        display_message(message)
        if value != "":
            print("Leave empty for current: {}".format(value))
        text = input("Enter the task {}: ".format(title))
        if text.strip() == "":
            if value != "":
                text = value
            elif required is True:
                message = "Task {} cannot be empty.".format(title)
                continue
        if type == "number" and not text.isnumeric():
            message = "Task {} must be a number.".format(title)
            continue
        if type == "date" and not is_valid_date(text):
            message = ("Invalid date {}. Date must be in the format "
                       "YYYY-MM-DD.".format(text))
            continue
        return text