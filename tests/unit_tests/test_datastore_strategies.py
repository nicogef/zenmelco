import unittest

from store.datastore_strategies import UniqueIdentifierIndexing, MultiIdentifierIndexing, ListIndexing
from store.datastore_strategies import as_string, as_int, as_boolean, INT_DEFAULT, STRING_DEFAULT, BOOLEAN_DEFAULT
from store.datastore_load import Element
import datetime

class TestDatastoreSearchStrategy(unittest.TestCase):
    
    def test_datastore_strategies_element(self):
        element = Element({"ABC" : "DEF"}, "ABC")
        self.assertEqual(element.get_description(), "DEF")
        self.assertEqual(element.get_data(), {"ABC" : "DEF"})


    def test_datastore_strategies_as_int(self):
        self.assertEqual(as_int(None), INT_DEFAULT)
        self.assertEqual(as_int(""), INT_DEFAULT)
        self.assertEqual(as_int("1"), 1)
        self.assertEqual(as_int(1), 1)
        self.assertEqual(as_int("2016-05-11T12:16:15 -10:00"), 1463004975)
        from store.datastore_context import DatastoreError
        with self.assertRaises(DatastoreError) as context:
            as_int("text")
        self.assertEqual(str(context.exception), "'text' is invalid as an 'INT' identifier")
        
    def test_datastore_strategies_as_string(self):
        # Corner cases
        self.assertEqual(as_string(""), STRING_DEFAULT)
        self.assertEqual(as_string(1), "1")
        self.assertEqual(as_string(False), STRING_DEFAULT)
        self.assertEqual(as_string("Test"), "Test")
                
    def test_datastore_strategies_as_boolean(self):
        # Corner cases
        self.assertEqual(as_boolean(None), BOOLEAN_DEFAULT)
        self.assertEqual(as_boolean(""), BOOLEAN_DEFAULT)
        self.assertEqual(as_boolean(True), "True")
        self.assertEqual(as_boolean("True"), "True")
        self.assertEqual(as_boolean("true"), "True")
        self.assertEqual(as_boolean(False), "False")
        self.assertEqual(as_boolean("false"), "False")
        self.assertEqual(as_boolean("False"), "False")
        from store.datastore_context import DatastoreError
        with self.assertRaises(DatastoreError) as context:
            as_boolean("text")
        self.assertEqual(str(context.exception), "'text' is invalid as a 'BOOLEAN' identifier")

    def test_datastore_strategies_unique_identifier(self):
        strategy = UniqueIdentifierIndexing("Test", as_string)
        element = Element({"Test" : "ABC"}, "Test")
        strategy.add(element)
        from store.datastore_context import DatastoreError
        with self.assertRaises(DatastoreError) as context:
            strategy.add(element)
        self.assertEqual('Unique Identifiers cannot have 2 identical values Test - ABC', str(context.exception))
        self.assertEqual(strategy.get("ABC"), [element])
        self.assertEqual(strategy.key(), "Test")
        self.assertEqual(strategy.default(), STRING_DEFAULT)

    def test_datastore_strategies_multi_value(self):
        strategy = MultiIdentifierIndexing("Test", as_int)
        element = Element({"Test" : 1}, "Test")
        strategy.add(element)
        strategy.add(element)
        self.assertEqual(strategy.get("1"), [element, element])
        self.assertEqual(strategy.key(), "Test")
        self.assertEqual(strategy.default(), INT_DEFAULT)

    def test_datastore_strategies_date_value(self):
        strategy = MultiIdentifierIndexing("date", as_int)
        element = Element({"date" : "2016-05-11T12:16:15 -10:00"}, "Test")
        strategy.add(element)
        strategy.add(element)
        self.assertEqual(strategy.get("2016-05-11T12:16:15 -10:00"), [element, element])
        self.assertEqual(strategy.key(), "date")
        self.assertEqual(strategy.default(), INT_DEFAULT)

    def test_datastore_strategies_boolean_value(self):
        strategy = MultiIdentifierIndexing("bool", as_boolean)
        element = Element({"bool" : False}, "Test")
        element2 = Element({"bool" : ""}, "Test")
        strategy.add(element)
        strategy.add(element2)
        self.assertEqual(strategy.get(False), [element])
        self.assertEqual(strategy.key(), "bool")
        self.assertEqual(strategy.default(), BOOLEAN_DEFAULT)
        self.assertEqual(strategy.get("Empty"), [element2])
        
    def test_datastore_strategies_list(self):
        strategy = ListIndexing("list")
        element = Element({"list" : ["ABC", "DEF", "GHI"]}, "Test")
        strategy.add(element)
        strategy.add(element)
        self.assertEqual(strategy.get("ABC"), [element, element])
        self.assertEqual(strategy.get("ABC"), [element, element])
        self.assertEqual(strategy.key(), "list")


