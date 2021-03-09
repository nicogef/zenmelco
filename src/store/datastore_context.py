from abc import ABCMeta, abstractmethod

class DatastoreWarning(Exception):
    ''' Simple Custom exception to manage Menu level Errors. '''
    pass

class DatastoreError(Exception):
    ''' Simple Custom exception to manage Menu level Errors. '''
    pass

class DatastoreAccess(metaclass=ABCMeta):
    ''' Defines the contract between the User Interface and the data store. '''
    @abstractmethod
    def entities(self)-> []:
        ''' Returns the list of available entities. '''
        pass

    @abstractmethod
    def search(self, entity: str, item: str, value: str)-> {}:
        ''' Returns the pair (key, value) associated to the request. '''
        pass

    @abstractmethod
    def field_list(self, entity: str)-> []:
        ''' Returns the list of fields associated to the entity. '''
        pass

class DatastoreElement(metaclass=ABCMeta):
    def __init__(self, element):
        self.data = element

    @abstractmethod
    def export(self, formatter):
        pass

class DatastoreResult():
    def __init__(self):
        self.elements = []
    
    def append(self, element):
        self.elements.append(element)

    def export(self, formatter):
        if not self.elements:
            print("No Results found")
        else:
            for element in self.elements:
                element.export(formatter)