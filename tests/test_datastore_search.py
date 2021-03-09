import unittest

from store.datastore import Datastore
from store.datastore_load import DatastoreLoader
from store.datastore_context import DatastoreWarning

class VerifResultHelper():
    ''' Helper class to simplify the result verification. '''
    def __init__(self, number_of_lines):
        self.number_of_lines = number_of_lines
        self.fields = []
        self.links = []

    def with_field(self, key, value):
        self.fields.append((key, value))
        return self

    def with_links(self, key, value):
        self.links.append((key, value))
        return self

class TestDatastoreSearch(unittest.TestCase):

    def setUp(self):
        self.datastore = Datastore(DatastoreLoader().load("resources"))

    def test_datastore_search_incorrect_Entity(self):
        ''' Checks the management of an unknwon entity. '''
        with self.assertRaises(DatastoreWarning) as context:
            self.datastore.search("Test", "", "")
        self.assertEqual("Entity 'Test' does not exists in the data store", str(context.exception))
        
    def test_datastore_search_incorrect_Item(self):
        ''' Checks that all the json files have been loaded with an indexation in Title case. '''
        with self.assertRaises(DatastoreWarning) as context:
            self.datastore.search("Users", "Test2", "")
        self.assertEqual("Field 'Test2' does not exists in entity 'Users' of the data store", str(context.exception))

    def test_datastore_search_tickets(self):
        ''' Checks the return result of the search method '''
        checker = []
        checker.append(VerifResultHelper(16) \
                            .with_field("_id", "8ea53283-5b36-4328-9a78-f261ee90f44b") \
                            .with_field("subject", "A Catastrophe in Sierra Leone") \
                            .with_links("submitter_id", 
                                {"user_name" : "Key Mendez"}) \
                            .with_links("assignee_id", 
                                {"user_name" : "Prince Hinton"}) \
                            .with_links("organization_id", 
                                {"organization_name" : "Bitrex"}))
        self.assert_datastore_search("Tickets", "_id", "8ea53283-5b36-4328-9a78-f261ee90f44b", checker)
        
    def test_datastore_search_users(self):
        checker = []
        checker.append(VerifResultHelper(19) \
                            .with_field("_id", 71) \
                            .with_field("name", "Prince Hinton") \
                            .with_links("submitter_id",
                                {"ticket_0" : "A Catastrophe in Micronesia",
                                 "ticket_1" : "A Drama in Wallis and Futuna Islands",
                                 "ticket_2" : "A Drama in Australia"}) \
                            .with_links("assignee_id", 
                                {"ticket_0" : "A Catastrophe in Sierra Leone"}) \
                            .with_links("organization_id", 
                                {"organization_name" : "HotcÃ¢kes"}))
        self.assert_datastore_search("Users", "_id", "71", checker)


    def test_datastore_search_orgnizations(self):
        checker = []
        checker.append(VerifResultHelper(9) \
                            .with_field("_id", 124) \
                            .with_field("name", "Bitrex") \
                            .with_links("organization_id",
                                {"ticket_0" : "A Nuisance in Egypt",
                                 "ticket_1" : "A Drama in Georgia",
                                 "ticket_2" : "A Drama in Germany",
                                 "ticket_3" : "A Catastrophe in Sierra Leone",
                                 "ticket_4" : "A Catastrophe in Central African Republic",
                                 "ticket_5" : "A Catastrophe in Belize",
                                 "ticket_6" : "A Problem in Marshall Islands",
                                 "ticket_7" : "A Catastrophe in Tuvalu",
                                 "ticket_8" : "A Problem in Saint Kitts and Nevis",
                                 "ticket_9" : "A Catastrophe in Netherlands Antilles",
                                 "user_0" : "Francis RodrigÃ¼ez",
                                 "user_1" : "Russo Vincent",
                                 "user_2" : "Jennifer Gaines",
                                 "user_3" : "Harper Sandoval",
                                 "user_4" : "Spence Tate"}))
        self.assert_datastore_search("Organizations", "_id", "124", checker)

    def test_datastore_search_no_description(self):
        checker = []
        checker.append(VerifResultHelper(16) \
                            .with_field("_id", "4cce7415-ef12-42b6-b7b5-fb00e24f9cc1") \
                            .with_field("subject", "A Nuisance in Ghana") \
                            .with_field("description", "") \
                            .with_links("submitter_id", 
                                {"user_name" : "Josefa Mcfadden"}) \
                            .with_links("assignee_id", 
                                {"user_name" : "Pitts Park"}) \
                            .with_links("organization_id", 
                                {"organization_name" : "Xylar"}))
        self.assert_datastore_search("Tickets", "description", "", checker)

    def test_datastore_search_regression(self):
        # Empty Int
        self.assertEqual(len(self.datastore.search("Tickets", "assignee_id", "").elements), 4)
        self.assertEqual(len(self.datastore.search("Tickets", "assignee_id", "24").elements), 4)
        # Empty String
        self.assertEqual(len(self.datastore.search("Tickets", "description", "").elements), 1)
        # Empty Link
        self.assertEqual(len(self.datastore.search("Tickets", "type", "").elements), 2)
        self.assertEqual(len(self.datastore.search("Tickets", "type", "task").elements), 58)
        # Boolean
        self.assertEqual(len(self.datastore.search("Tickets", "has_incidents", "").elements), 0)
        self.assertEqual(len(self.datastore.search("Tickets", "has_incidents", "False").elements), 101)
        self.assertEqual(len(self.datastore.search("Tickets", "has_incidents", False).elements), 101)
        # Empty List
        self.assertEqual(len(self.datastore.search("Tickets", "tags", "").elements), 0)
        self.assertEqual(len(self.datastore.search("Tickets", "tags", "Ohio").elements), 14)
        # Empty Date
        self.assertEqual(len(self.datastore.search("Tickets", "created_at", "").elements), 0)
        self.assertEqual(len(self.datastore.search("Tickets", "created_at", "2016-06-26T12:12:53 -10:00").elements), 1)

    def assert_datastore_search(self, entity: str, item:str, value: str, checkers: VerifResultHelper):
        from store.datastore_context import DatastoreResult
        result = self.datastore.search(entity, item, value)
        # Assert the number of results
        self.assertIsInstance(result, DatastoreResult)
        self.assertEqual(len(result.elements), len(checkers))
        # Assert the number of fields
        for i in range(len(result.elements)):
            element = result.elements[i]
            checker = checkers[i]
            # Check record size
            self.assertEqual(len(element.data), checker.number_of_lines, "The number elements is incorrect")
            # Check Fields
            for (key, value) in checker.fields:
                self.assertEqual(element.data[key], value)
            # Check links
            for (key, value) in checker.links:
                self.assertTrue(key in element.links, f"link required for {key}")
                self.assertEqual(element.links[key], value, "Link invalid")

