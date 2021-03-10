import unittest

from unittest.mock import Mock
from store.datastore_strategies import as_string, as_int, as_boolean, UniqueIdentifierIndexing, MultiIdentifierIndexing, ListIndexing

from store.datastore_load import Entity
from store.datastore_configuration import FileConfiguration

class TestDatastoreList(unittest.TestCase):

    def setUp(self):
        fields = []
        fields.append(UniqueIdentifierIndexing("int", as_int))
        fields.append(MultiIdentifierIndexing("bool", as_boolean))
        fields.append(ListIndexing("string"))
        configuration = FileConfiguration(fields, None, None, None, None)
        self.entity = Entity(configuration)
        
    
    def test_datastore_load_entity(self):
        self.assertEqual(list(self.entity.field_list()), ["int","bool","string"])
        rawData = {
            "int" : 17,
            "bool": False,
            "string" : ["Some string", "Some other string"]
        }
        self.entity.add(rawData)
        self.assertEqual(self.entity.get_from_key("int", 17)[0].get_data(), rawData)
        self.assertEqual(self.entity.get_from_key("bool", False)[0].get_data(), rawData)
        self.assertEqual(self.entity.get_from_key("string", "Some string")[0].get_data(), rawData)
        self.assertEqual(self.entity.get_from_key("string", "Some other string")[0].get_data(), rawData)
        

