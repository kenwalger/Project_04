from io import StringIO
from unittest.mock import patch
from unittest import mock
import datetime
import unittest

import models
import helpers
import search
import task
import worklog


class TestDb(unittest.TestCase):
    # Create a test item - In process tests create
    def setUp(self):
        self.save_data = models.save(dict([('task_name', "unittest data"),
                                     ('user_name', "unittest data"),
                                     ('minutes', 0),
                                     ('notes', "unittest data"),
                                     ('date', "0000-01-01")]))

    # Delete our test item
    @patch('builtins.input', lambda x: 'y')
    def test_delete(self):
        """delete test data"""
        models.delete(self.save_data)
        check_delete = (models.Task.select()
                        .where((models.Task.task_name == "unittest data") &
                        (models.Task.date == "0000-01-01")))
        self.assertTrue(check_delete.count() == 0)


class TestFunctions(unittest.TestCase):
    """Tests the functions in functions.py"""

    # Test dates
    def test_is_valid_date(self):
        self.assertTrue(helpers.is_valid_date(str(datetime.date.today())))
        self.assertFalse(helpers.is_valid_date('garbage'))
        self.assertFalse(helpers.is_valid_date('0000-00-00'))
        self.assertFalse(helpers.is_valid_date('9999-99-99'))

    # Test headline is printed to screen
    def test_url_head_line_to_stdout(self):
        test_text = 'Fred at home'
        expected_out = 'Fred at home'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            helpers.header_line(test_text)
            self.assertIn(expected_out, fake_out.getvalue())

    # Test messages are displayed on screen
    def test_url_display_message_to_stdout(self):
        test_text = 'Fred at home'
        expected_out = 'Fred at home\n\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            helpers.display_message(test_text)
            self.assertIn(expected_out, fake_out.getvalue())

    # Test user input required, any text
    def test_user_input_required(self):
        fake_input = mock.Mock(side_effect=['', 'Test Text'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                test_case = helpers.edit("Input Title", "Header Text")
                self.assertEqual(fake_input.call_count, 2)
                self.assertIn('cannot be empty', fake_out.getvalue())

    # Test user input required, number
    def test_user_input_number(self):
        fake_input = mock.Mock(side_effect=['fred', '3'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                test_case = helpers.edit("Input Title", "Header Text",
                                         "number")
                self.assertEqual(fake_input.call_count, 2)
                self.assertIn('must be a number', fake_out.getvalue())

    # Test user input required, any valid date
    def test_user_input_date(self):
        fake_input = mock.Mock(side_effect=['fred', '3', '1234-56-78',
                                            '2014-01-01'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                test_case = helpers.edit("Input Title", "Header Text",
                                         "date")
                self.assertEqual(fake_input.call_count, 4)
                self.assertIn('Invalid date', fake_out.getvalue())

    # Test user input NOT required, return default
    @patch('builtins.input', lambda x: '')
    def test_user_input_not_required(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            test_case = helpers.edit("Input Title", "Header Text", "number",
                                     False, '123456')
            self.assertEqual(test_case, '123456')


class TestTask(unittest.TestCase):
    """Test our task class"""

    # Test new task, also tests displaying and deleting it
    def test_new_task(self):
        fake_input = mock.Mock(side_effect=['Test Task Name', 'Test User Name',
                                            '0', 'Test Task Notes'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                test_task = task.Task()
                self.assertEqual(fake_input.call_count, 4)
                test_task.delete_task()

    # Test load existing task and edit and view it
    def test_edit_task(self):
        data = models.save(dict([('task_name', 'task_name'),
                                 ('user_name', 'user_name'),
                                 ('minutes', 0),
                                 ('notes', 'notes'),
                                 ('date', datetime.date.today())]))
        fake_input = mock.Mock(side_effect=['0000-01-01',
                                            'Test Test Name Change',
                                            'Test User Name Change',
                                            '1000',
                                            'Test Task Notes Change', 'y'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                test_task = task.Task(task=data, header_line='header_line')
                test_task.edit_task()
                self.assertIn("Task Name: Test Test Name Change",
                              fake_out.getvalue())
                self.assertIn("User Name: Test User Name Change",
                              fake_out.getvalue())
                self.assertIn("Additional Notes: Test Task Notes Change",
                              fake_out.getvalue())
                self.assertIn("Minutes Taken: 1000", fake_out.getvalue())
                self.assertIn("Date: 0000-01-01", fake_out.getvalue())
                test_task.delete_task()


class TestLookup(unittest.TestCase):
    """Tests the functions in lookup.py for searching"""

    # Lookup by employee, select first and exit: Assumes data available
    def test_lookup_employee(self):
        fake_input = mock.Mock(side_effect=['', '1', 'q'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                search.employee()

    # Lookup by employee, non-existent or data not available
    def test_lookup_employee__no_match(self):
        fake_input = mock.Mock(side_effect=['^^∆©ß∑åπ…', ''])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                search.employee()

    # Lookup by date list, select first and exit: Assumes data available
    def test_lookup_date(self):
        fake_input = mock.Mock(side_effect=['1', 'q'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                search.date()

    # Lookup by search term: None found
    def test_lookup_search(self):
        fake_input = mock.Mock(side_effect=['¥®œ¬ø^~çç≈^¨¥®˚πµ√', ''])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                search.term()

    # Lookup by date range: Assumes data available
    def test_lookup_date_range(self):
        fake_input = mock.Mock(side_effect=['0000-01-01', '9999-12-31', '1',
                                            'n', 'p', 'q'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                search.date_range()


class TestMainProgram(unittest.TestCase):
    """Test our main program file"""

    # Test the main menu (Also covers testing the menu function)
    def test_main_menu(self):
        fake_input = mock.Mock(side_effect=['', '4', '3'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                worklog.run_app()
                self.assertEqual(fake_input.call_count, 3)
                self.assertIn("Sorry, your entry was not valid.",
                              fake_out.getvalue())
                self.assertIn("1. Record a new task entry.",
                              fake_out.getvalue())

    # Test the main menu (Also covers testing the menu function)
    def test_lookup_menu(self):
        fake_input = mock.Mock(side_effect=['6', '5'])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('builtins.input', fake_input):
                worklog.reports_menu()
                self.assertEqual(fake_input.call_count, 2)
                self.assertIn("Sorry, your entry was not valid.",
                              fake_out.getvalue())
                self.assertIn("Lookup previous task entries:",
                              fake_out.getvalue())

if __name__ == '__main__':
    unittest.main()
