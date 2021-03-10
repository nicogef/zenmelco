import io
import unittest
from unittest.mock import patch

class TestSubMenus(unittest.TestCase):

    def test_default_menu_init(self):
        ''' The program initialize correctly the Menus. '''
        from user_interface.menus import DefaultMenu
        menu = DefaultMenu("teSt")
        self.assertEqual(menu._intro, 'Enter search test (or "quit"):', "The value is expected to be added to the string in lower case.")
        self.assertEqual(menu._prompt, "Test> ", "The value is expected to be added to the String in title case.")
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_default_menu_prompt_validation(self, mock_out):
        ''' The program exists if 'quit'. '''
        from user_interface.menus import DefaultMenu
        from main_context import EXIT_TRIGGER
        menu = DefaultMenu("test2")
        
        self.assert_context_valid(menu, "", "")
        self.assert_context_valid(menu, "text", "text")
        self.assert_exit_program(menu, EXIT_TRIGGER)

    def test_entity_menu_init(self):
        ''' The program Builds correctly the Entity Menu. '''
        from user_interface.menus import EntityMenu
        menu = EntityMenu(["ABC","DEF","GHI"])
        result = '''Select Entity (or "quit"):
    1) ABC
    2) DEF
    3) GHI'''
        self.assertEqual(menu._intro, result, "The built value is incorrect.")
        self.assertEqual(menu._prompt, "Entity> ", "The value is expected to be added to the String in title case.")

    def test_entity_menu_with_all(self):
        ''' The program Builds correctly the Entity Menu (with All). '''
        from user_interface.menus import EntityMenu
        menu = EntityMenu(["ABC","DEF","GHI"]).with_all()
        result = '''Select Entity (or "quit"):
    1) ABC
    2) DEF
    3) GHI
    4) All'''
        self.assertEqual(menu._intro, result, "The built value is incorrect.")
        self.assertEqual(menu._prompt, "Entity> ", "The value is expected to be added to the String in title case.")

    def test_entity_menu_prompt_validation(self):
        ''' The program accepts valid indexes. '''
        from user_interface.menus import EntityMenu
        from main_context import EXIT_TRIGGER
        menu = EntityMenu(["ABC","DEF","GHI"])

        self.assert_context_invalid(menu, "", 'FORMAT_INVALID')
        self.assert_context_invalid(menu, "text", 'FORMAT_INVALID')
        self.assert_context_invalid(menu, "-1", 'FORMAT_INVALID')
        self.assert_context_invalid(menu, "0", 'INDEX_OUT_OF_RANGE')
        # Valid cases
        self.assert_context_valid(menu, "1", "ABC")
        self.assert_context_valid(menu, "2", "DEF")
        self.assert_context_valid(menu, "3", "GHI")
        self.assert_context_invalid(menu, "4", 'INDEX_OUT_OF_RANGE')
        # Add the last menu item.
        menu.with_all()
        self.assert_context_valid(menu, "4", "ABC,DEF,GHI")
        self.assert_exit_program(menu, EXIT_TRIGGER)

    def assert_context_invalid(self, menu, value, assertion):
        ''' Gneric method to perform EntityMenu validation tests. '''
        from user_interface.menu_context import MenuContextWarning
        with self.assertRaises(MenuContextWarning) as context:
            # Hide sys.stdout
            with patch('sys.stdout', new_callable=io.StringIO) as _:
                with patch('builtins.input', return_value=value):
                    menu.prompt()
        self.assertEqual(assertion, str(context.exception), f"{assertion} expected for value {value}")
        
    def assert_exit_program(self, menu, value):
        ''' Gneric method to perform EntityMenu validation tests. '''
        from main_context import ExitProgram
        with self.assertRaises(ExitProgram) as context:
            # Hide sys.stdout
            with patch('sys.stdout', new_callable=io.StringIO) as _:
                with patch('builtins.input', return_value=value):
                    menu.prompt()
        self.assertEqual('Exit Program upon User request.', str(context.exception))

    def assert_context_valid(self, menu, value, assertion):
        ''' Gneric method to perform EntityMenu validation tests. '''
        # Hide sys.stdout
        result = ""
        with patch('sys.stdout', new_callable=io.StringIO) as _:
            with patch('builtins.input', return_value=value):
                result = menu.prompt()
        self.assertEqual(assertion, result, f"{assertion} is expected for {value}")