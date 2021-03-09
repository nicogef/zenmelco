import os
import json

from store.datastore_configuration import get_configuration, FileConfiguration
from store.datastore_strategies import Element

def load(resourcesPath: str) -> {}:
    ''' Loads all json files in the "resource" folder and initialise the Search strategies. '''
    datastores = {}
    for root, _, files in os.walk(resourcesPath):
        json_files = [f for f in files if ".json" in f]
        for f in json_files:
            with open(os.path.join(root, f) ,"r") as json_file:
                entity_name = os.path.splitext(f)[0].title()
                entity = Entity(get_configuration(entity_name))
                for obj_json in json.load(json_file):
                    entity.add(obj_json)
                datastores[entity_name] = entity
    return datastores

class Entity():
    ''' Provides the services to read, store and access the data.
    
        Arguments:
        - configuration: The configuration for each loaded file.
    '''
    def __init__(self, configuration: FileConfiguration):
        self._fields = {}
        for strategy in configuration.fields:
            self._fields[strategy.key()] = strategy
        self._out_links = configuration.out_links
        self._in_links = configuration.in_links
        self.description_field_name = configuration.description
        self.name = configuration.name
    
    def field_list(self) -> []:
        ''' Returns the list of keys in the store. '''
        return self._fields.keys()

    def add(self, rawData):
        '''Initialise the data and the data Search Strategies. ''' 
        element = self._convert(rawData)
        for field in self._fields:
            self._fields[field].add(element)
    
    def _convert(self, rawData):
        ''' Converts the received raw Data into an internal element. '''
        for field in self._fields:
            if not field in rawData:
                rawData[field] = self._fields[field].default()
        return Element(rawData, self.description_field_name)

    def get_from_key(self, key, value) -> []:
        ''' Retrieve an element from the datastore. '''
        return self._fields[key].get(value)
    
    def in_links(self):
        return self._in_links

    def out_links(self):
        return self._out_links

    def get_name(self):
        return self.name
    
    def get_description_field_name(self):
        return self.description_field_name