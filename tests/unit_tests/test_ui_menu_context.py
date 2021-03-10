import io
import unittest
from unittest.mock import patch

class TestSubMenuContext(unittest.TestCase):

    def test_menu_context_menu_warning(self):
        ''' The program resumes upon menu Warning. '''
        from user_interface.menu_context import MenuContext, MenuContextWarning
        with patch('sys.stdout', new_callable=io.StringIO) as _:
            with MenuContext():
                raise MenuContextWarning("Warning")

    def test_menu_context_datastore_warning(self):
        ''' The program resumes upon Datastore Warning. '''
        from user_interface.menu_context import MenuContext
        from store.datastore_context import DatastoreWarning
        with patch('sys.stdout', new_callable=io.StringIO) as _:
            with MenuContext():
                raise DatastoreWarning("Search_error")

    def test_menu_context_datastore_error(self):
        ''' The program exists on exit request from the Menu context. '''
        from user_interface.menu_context import MenuContext
        from store.datastore_context import DatastoreError
        with self.assertRaises(DatastoreError) as context:
            with MenuContext():
                raise DatastoreError("Some Error")
        self.assertEqual('Some Error', str(context.exception))
            
    def test_menu_context_exit(self):
        ''' The program exists on exit request from the Menu context. '''
        from user_interface.menu_context import MenuContext
        from main_context import ExitProgram
        with self.assertRaises(ExitProgram) as context:
            with MenuContext():
                raise ExitProgram("Exit")
        self.assertEqual('Exit', str(context.exception))
                    
    def test_menu_context_exception(self):
        ''' The program does not hide all exceptions. '''
        from user_interface.menu_context import MenuContext
        with self.assertRaises(Exception) as context:
            with MenuContext():
                raise Exception("Any other exception")
        self.assertEqual('Any other exception', str(context.exception))

