from cmd import Cmd
from abc import ABCMeta 
from main_context import MAIN_MENU_INTRO, MAIN_MENU_PROMPT, exit_program, Console, EXIT_TRIGGER
from user_interface.menu_context import MenuContextWarning, MenuContext
from store.datastore_context import DatastoreAccess, DatastoreWarning
import timeit

class MainMenu(Cmd):
    ''' Main menu manage the User actions. '''
    prompt = MAIN_MENU_PROMPT
    intro  = MAIN_MENU_INTRO
    EXIT = True    
    CONTINUE = False

    def __init__(self, datastore: DatastoreAccess):
        super(MainMenu, self).__init__()
        self.datastore = datastore

    def do_quit(self, inp):
        ''' Type 'quit' to exit '''
        exit_program(EXIT_TRIGGER)

    def do_1(self, inp):
        ''' Performs the search of a value in the request Entity for a specified term. '''
        with MenuContext():
            entity = EntityMenu(self.datastore.entities()).prompt()
            term = DefaultMenu("Term").prompt()
            value = DefaultMenu("Value").prompt()

            start = timeit.default_timer()
            search_result = self.datastore.search(entity, term, value)
            took = (timeit.default_timer() - start) * 1000.0
            search_result.export(Console)
            print(f"Search performed in {took:8.3f} ms with {len(search_result.elements)} results")
        return MainMenu.CONTINUE

    def do_2(self, inp):
        ''' Displays the searchable fields. '''
        print(f'List of Searchable fields')
        with MenuContext():
            entities = EntityMenu(self.datastore.entities()).with_all().prompt()
            
            search_result = self.datastore.field_list(entities)
            search_result.export(Console)
        return MainMenu.CONTINUE

class DefaultMenu(metaclass=ABCMeta):
    ''' Provides a Menu for a simple prompt to retrieve a String. '''
    def __init__(self, prompt):
        self._prompt = prompt.title() + "> "
        self._intro  = self._build_intro(prompt)

    def prompt(self) -> bool:
        ''' Prompts the user, check the input and return the result. '''
        print(self._intro)
        rtn = exit_program(input(self._prompt))
        return self._validate(rtn)

    def _validate(self, value) -> str:
        ''' Validates the expected value for a specific Menu. '''
        return value
    
    def _build_intro(self, prompt):
        ''' Builds the introduction '''
        return f'Enter search {prompt.lower()} (or "quit"):'
        
class EntityMenu(DefaultMenu):
    ''' Provides a Menu to choose the entity loaded in the datastore. '''
    def __init__(self, values):
        self._mapping = []
        self.values = values
        super().__init__('Entity')

    def _build_intro(self, prompt):
        ''' Defines a custom introduction. '''
        intro= 'Select Entity (or "quit"):'
        for i in range(len(self.values)):
            intro += self._format(i, self.values[i])
            self._mapping.append(self.values[i])
        return intro

    def _validate(self, value) -> str:
        ''' Custom Validation and conversion of the entity value. '''
        if value.isnumeric():
            index = int(value) - 1
            if 0 <= index and index < len(self._mapping):
                return self._mapping[index]
            else:
                raise MenuContextWarning("INDEX_OUT_OF_RANGE")
        raise MenuContextWarning("FORMAT_INVALID")
    
    def with_all(self):
        self._intro += self._format(len(self._mapping), "All")
        self._mapping.append(",".join(self._mapping))
        return self

    def _format(self, id, string):
        return f'\n    {id + 1}) {string}'