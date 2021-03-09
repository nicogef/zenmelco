import unittest

from store.datastore import Datastore
from store.datastore_load import load
from store.datastore_context import DatastoreWarning

class TestDatastoreList(unittest.TestCase):

    def setUp(self):
        self.datastore = Datastore(load("resources"))

    def test_datastore_entities(self):
        ''' Checks that all the json files have been loaded with an indexation in Title case. '''
        self.assertListEqual(["Organizations", "Tickets", "Users"], self.datastore.entities(), "The datastore has not been initialised properly.")
        
    def test_datastore_list_invalid_Entities(self):
        ''' Checks that all the json files have been loaded with an indexation in Title case. '''
        with self.assertRaises(DatastoreWarning) as context:
            self.datastore.field_list("Test")
        self.assertEqual("Entity 'Test' does not exists in the data store", str(context.exception))
        
    def test_datastore_list_valid_Entities(self):
        ''' Checks that all the json files have been loaded with an indexation in Title case. '''
        self.assert_datastore_list("Users", [19])
        self.assert_datastore_list("Users,Tickets", [19, 16])
        self.assert_datastore_list("Users,Tickets,Organizations", [19, 16, 9])

    def assert_datastore_list(self, value: str, data: []):
        from store.datastore_context import DatastoreResult
        result = self.datastore.field_list(value)
        # Assert the number of results
        self.assertIsInstance(result, DatastoreResult, "The return result is of an invalid type")
        self.assertEqual(len(result.elements), len(data), "The number of elements is not correct")
        # Assert the number of fields
        for i in range(len(result.elements)):
            self.assertEqual(len(result.elements[i].data), data[i], "The number elements is incorrect")
