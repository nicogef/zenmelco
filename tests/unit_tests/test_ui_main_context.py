import io
import unittest
from unittest.mock import patch

class TestMainContext(unittest.TestCase):
            
    def test_main_context_exit(self):
        ''' The program manage a clean exit. '''
        from main_context import MainContext, ExitProgram
        with patch('sys.stdout', new_callable=io.StringIO) as _:
            with MainContext():
                raise ExitProgram("Warning")

    def test_main_context_menu_warning(self):
        ''' The program does not hide an invalid MenuWarning. '''
        from main_context import MainContext
        from user_interface.menu_context import MenuContextWarning
        with self.assertRaises(MenuContextWarning) as context:
            with MainContext():
                raise MenuContextWarning("Exit")
        self.assertEqual('Exit', str(context.exception))

    def test_main_context_datastore_warning(self):
        ''' The program does not hide an invalid Search. '''
        from main_context import MainContext
        from store.datastore_context import DatastoreWarning
        with self.assertRaises(DatastoreWarning) as context:
            with MainContext():
                raise DatastoreWarning("Exit")
        self.assertEqual('Exit', str(context.exception))

    def test_main_context_datastore_error(self):
        ''' The program exits if the exit function is called with the exit trigger. '''
        from main_context import MainContext
        from store.datastore_context import DatastoreError
        with self.assertRaises(DatastoreError) as context:
            raise DatastoreError("Some Error")
        self.assertEqual('Some Error', str(context.exception))
                    
    def test_main_context_exception(self):
        ''' The program does not hide all exceptions. '''
        from main_context import MainContext
        with self.assertRaises(Exception) as context:
            with MainContext():
                raise Exception("Any other exception")
        self.assertEqual('Any other exception', str(context.exception))
    
    def test_exit_with_quit(self):
        ''' The program exits if the exit function is called with the exit trigger. '''
        from main_context import exit_program, EXIT_TRIGGER, ExitProgram
        with self.assertRaises(ExitProgram) as context:
            exit_program(EXIT_TRIGGER)
        self.assertEqual('Exit Program upon User request.', str(context.exception))

    def test_no_exit_with_string(self):
        ''' The program does not exits if the exit function is called with a random string. '''
        from main_context import exit_program
        self.assertEqual(exit_program("anything"), "anything")