import unittest

from store.datastore_load import Element

class TestDatastoreList(unittest.TestCase):

    def test_datastore_load_element(self):
        element = Element({"ABC" : "DEF"}, "ABC")
        self.assertEqual(element.get_description(), "DEF")
        self.assertEqual(element.get_data(), {"ABC" : "DEF"})
