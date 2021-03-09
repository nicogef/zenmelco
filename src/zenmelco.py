from main_context import MainContext, Console
from store.datastore_load import load
from store.datastore import Datastore
from user_interface.menus import MainMenu

if __name__ == "__main__":
    with MainContext():
        datastore = Datastore(load("resources"))
        MainMenu(datastore).cmdloop()
    

