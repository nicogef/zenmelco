from store.datastore_context import DatastoreWarning

class MenuContextWarning(Exception):
    ''' Simple Custom exception to manage Menu level Errors. '''
    pass

class MenuContext(object):
    ''' Sub Menu context manager.
            Displays the Menu Custom exception and ignores it. 
    '''
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type and exc_type == MenuContextWarning or exc_type == DatastoreWarning:
            print(f"Warning: Cancel request due to {exc_value}")
            print("---")
            # Supress Exception
            return True

