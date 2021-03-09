from main_context import MainContext, Console
from store.datastore_load import DatastoreLoader
from store.datastore import Datastore
from user_interface.menus import MainMenu

if __name__ == "__main__":
    with MainContext():
        data = DatastoreLoader().load("resources")
        datastore = Datastore(data)
        MainMenu(datastore).cmdloop()
    

