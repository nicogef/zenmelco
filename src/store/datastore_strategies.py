from abc import ABCMeta, abstractmethod
from store.datastore_context import DatastoreError
import datetime

#################################
# Conversion and default values
#################################
DATE_DEFAULT = "1900-01-01T00:00:00-00:00"
INT_DEFAULT = 0
STRING_DEFAULT = ""
LIST_DEFAULT = []
BOOLEAN_DEFAULT = "Empty"

def as_int(value):
    if value is None or value == "":
        return INT_DEFAULT
    elif isinstance(value, int) or value.isnumeric():
        return int(value)
    else:
        try:
            return int(datetime.datetime.fromisoformat(value).timestamp())
        except ValueError:
            raise DatastoreError(f"'{value}' is invalid as an 'INT' identifier")

def as_string(value):
    return str(value) if value else STRING_DEFAULT

def as_list(value):
    return value

def as_boolean(value):
    if value is None or value == "":
        return BOOLEAN_DEFAULT
    try:
        return str(value)
    except ValueError:
        raise DatastoreError(f"'{value}' is invalid as a BOOLEAN identifier")
    
class Element():
    ''' Stores an Element of the datastore. '''
    def __init__(self, data, description):
        self._data = data
        self._description = description

    def get_data(self):
        return self._data

    def get_description(self):
        return self._data[self._description]

class IndexingStrategy(metaclass=ABCMeta):
    def __init__(self, key, index):
        self._key = key
        self._to_index = index
        self._element_dict = {}

    @abstractmethod
    def _add(self, value, element: Element):
        pass

    def add(self, element):
        self._add(self._to_index(element.get_data()[self._key]), element)

    def get(self, value) -> []:
        v = self._to_index(value)
        if not v in self._element_dict:
            return []
        return self._element_dict[v]

    def key(self):
        return self._key

    def default(self):
        return self._to_index(None)

class UniqueIdentifierIndexing(IndexingStrategy):
    def __init__(self, key, index):
        super().__init__(key, index)

    def _add(self, value, element):
        if value in self._element_dict:
            raise DatastoreError(f"Unique Identifiers cannot have 2 identical values {self._key} - {value}")
        self._element_dict[value] = [element]

class MultiIdentifierIndexing(IndexingStrategy):
    def __init__(self, key, index):
        super().__init__(key, index)

    def _add(self, value, element):
        if not value in self._element_dict:
            self._element_dict[value] = []
        self._element_dict[value].append(element)

class ListIndexing(MultiIdentifierIndexing):
    def __init__(self, key):
        super().__init__(key, as_list)

    def _add(self, value, element):
        for v in value:
            super(ListIndexing, self)._add(v, element)