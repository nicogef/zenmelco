from store.datastore_context import DatastoreError

#################################################
# TRIGGERS
#################################################
EXIT_TRIGGER="quit"

#################################################
# MAIN MENU
#################################################
MAIN_MENU_PROMPT = 'search option> '
MAIN_MENU_INTRO=f"""
Welcome! This tool will help you to search in the datastore.
Type '{EXIT_TRIGGER}' to exit at any time, Press 'Enter' to continue.

        Select search options:
        * Press 1 to search Zendesk
        * Press 2 to view a list of searchable fields
        * Type '{EXIT_TRIGGER}' to exit
"""

#################################################
# Exit Function
#################################################
class ExitProgram(Exception):
    ''' Custom exception to manage Program Exit. '''

def exit_program(item=None) -> str:
    ''' Checks if the user requested to exit the program. 

        Arguments:
            - item (Optional) - exists only if:
                - not present
                - equal to 'ExitProgram.EXIT_TRIGGER'
            
    '''
    if item == EXIT_TRIGGER:
        raise ExitProgram("Exit Program upon User request.")
    return item

#################################################
# MAIN CONTEXT
#################################################
class MainContext(object):
    ''' Exit context manager. 
            Manage a clean exit from anywhere in the program upon user request requested.
    '''
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type: 
         if exc_type == ExitProgram:
            print("Exit program upon User request.")
            # Suppress Exception
            return True
        elif exc_type == DatastoreError:
            print(f"Exit program upon initialisation Error. \n    => {exc_value}")
            # Do not Suppress Exception
            return False

#################################################
# Print Strategy (Console)
#################################################
class Console():
    @staticmethod
    def as_dict(d, indent=0):
        for key, value in d.items():
            if isinstance(value, dict):
                print('\t' * indent + str(key))
                Console.as_dict(value, indent+1)
            else:
                print('\t' * indent + f"{key:20}{value}")

    @staticmethod
    def as_list(d):
        print("\n".join(d))

    @staticmethod
    def as_line(d):
        print(d)