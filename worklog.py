#!/usr/bin/env python3
""" 
Worklog with a database
Techdegree Project 04

Nov 2016

"""

import helpers
import search
import task


def run_app():
    while True:
        menu_choice = helpers.menu(
            "Main Menu:",
            "Record a new task entry.",
            "Lookup previous task entries.",
            "Exit the program."
            )

        if int(menu_choice) == 1:
            new_task = task.Task()

        if int(menu_choice) == 2:
            reports_menu()

        if int(menu_choice) == 3:
            helpers.clear_screen()
            break


def reports_menu():
    while True:
        menu_search = helpers.menu(
            "Lookup previous task entries:",
            "Find by employee.",
            "Find by date.",
            "Find by search term.",
            "Find by date range.",
            "Return to main menu."
            )

        if int(menu_search) == 1:
            result = search.employee()

        if int(menu_search) == 2:
            result = search.date()

        if int(menu_search) == 3:
            result = search.term()

        if int(menu_search) == 4:
            result = search.date_range()

        if int(menu_search) == 5:
            helpers.clear_screen()
            break

# Call the main function if run directly
if __name__ == '__main__':
    run_app()
