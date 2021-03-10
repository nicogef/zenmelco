import io
import unittest
from unittest.mock import patch, Mock
class TestMainMenu(unittest.TestCase):

    def test_main_menu_init(self):
        ''' The program Builds correctly the Entity Menu. '''
        from user_interface.menus import MainMenu
        db = Mock()
        menu = MainMenu(db)
        self.assertEqual(menu.prompt, 'search option> ')
        self.assertEqual(menu.intro, f"""
Welcome! This tool will help you to search in the datastore.
Type 'quit' to exit at any time, Press 'Enter' to continue.

        Select search options:
        * Press 1 to search Zendesk
        * Press 2 to view a list of searchable fields
        * Type 'quit' to exit
""")

    def test_main_menu_quit(self):
        ''' The program Builds correctly the Entity Menu. '''
        from user_interface.menus import MainMenu
        from main_context import ExitProgram
        db = Mock()
        menu = MainMenu(db)
        with self.assertRaises(ExitProgram) as _:
            menu.do_quit(None)
            
    def test_main_menu_search(self):
        ''' The program Calls the datastore with the correct values. '''
        from user_interface.menus import MainMenu
        from store.datastore_context import DatastoreResult
        db = Mock()
        db.entities.return_value = ["ABC","DEF","GHI"]
        db.search.return_value = DatastoreResult()
        menu = MainMenu(db)
        with patch('sys.stdout', new_callable=io.StringIO) as _:
            with patch('builtins.input', side_effect=["1", "Test", "A Value"]):
                menu.do_1(None)
        db.entities.assert_called_once()
        db.search.assert_called_once_with("ABC", "Test", "A Value")
        db.field_list.assert_not_called()
                    
    def test_main_menu_list(self):
        ''' The program Calls the datastore with the correct values. '''
        from user_interface.menus import MainMenu
        from store.datastore_context import DatastoreResult
        db = Mock()
        db.entities.return_value = ["ABC","DEF","GHI"]
        db.field_list.return_value = DatastoreResult()
        menu = MainMenu(db)
        with patch('sys.stdout', new_callable=io.StringIO) as _:
            with patch('builtins.input', side_effect=["2"]):
                menu.do_2(None)
        db.entities.assert_called_once()
        db.search.assert_not_called()
        db.field_list.assert_called_once_with("DEF")