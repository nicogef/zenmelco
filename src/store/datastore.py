import os
import json
import datetime

from store.datastore_context import DatastoreWarning, DatastoreAccess, DatastoreElement, DatastoreResult, DatastoreError
from store.datastore_load import Element

class Datastore(DatastoreAccess):
    def __init__(self, datastore: {}):
        ''' Initialise the list of Entity by loading all the json files from the resources folder.

                resourcesPath
                    The relative path to the resources.
        '''
        self._datastore = datastore

    def entities(self)-> []:
        ''' Returns the list of Entities in memory. '''
        return list(self._datastore.keys())
        
    def search(self, entity_name: str, item: str, value: str)-> DatastoreResult:
        ''' Search the datastore with the provided arguments. '''
        print(f'Searching "{entity_name.lower()}" for "{item}" with a value of "{value}"')
        if not entity_name in self._datastore:
            raise DatastoreWarning(f"Entity '{entity_name}' does not exists in the data store")
        
        entity = self._datastore[entity_name]
        if not item in entity.field_list():
            raise DatastoreWarning(f"Field '{item}' does not exists in entity '{entity_name}' of the data store")

        search_result = []
        if " or " in value:
            searches = value.split(" or ")
            for search in searches:
                search_result.extend(entity.get_from_key(item, search))
        elif  " and " in value:
            searches = value.split(" and ")
            for search in searches:
                result = entity.get_from_key(item, search)
                if search_result == []:
                    search_result = result
                else:
                    new_result = []
                    for element1 in result:
                        for element2 in search_result:
                            if element2 is element1:
                                new_result.append(element1)
                    search_result = new_result
        else:
            search_result.extend(entity.get_from_key(item, value))



        return self._format_and_add_links(entity, search_result)

    def field_list(self, entity_names: str)-> DatastoreResult:
        ''' 
        Returns the list of fields associated for each specified entity. 
        
            Arguments:
            - entity_names: str, The entities for which to display the fields.
        '''
        results = DatastoreResult()
        for entity_name in entity_names.split(","):
            if not entity_name in self._datastore:
                raise DatastoreWarning(f"Entity '{entity_name}' does not exists in the data store")
            results.append(ListElementResult(self._datastore[entity_name].field_list(), entity_name))

        return results

    def _format_and_add_links(self, entity, elements):
        ''' Formats the Result into a simple list of elements and add the links to the object. '''
        results = DatastoreResult()
        for element in elements:
            result = SearchElementResult(element)

            # ASS2 - Out links are refers to a unique record.
            for (link, store) in entity.out_links().items():
                result.with_out_link(self._datastore[store], link)
            
            # ASS3 - In links can be refered from multiple records.
            for (link, stores) in entity.in_links().items():
                for store in stores.split(","):
                    result.with_in_link(self._datastore[store], link)
            results.append(result)
        return results

class SearchElementResult(DatastoreElement):
    ''' Holds a result element with the associated links to related entities. '''
    def __init__(self, element: Element):
        super().__init__(element.get_data())
        self.links = {}

    def with_out_link(self, store, link):
        element = store.get_from_key("_id", self.data[link])
        if len(element) == 1:
            _id = f'{store.get_name()}_{store.get_description_field_name()}'
            self._add_link(link, _id, element[0])
        elif len(element) > 1:
            raise DatastoreError("Error in out_links, this should be unique")
        return self

    def with_in_link(self, store, link):
        elements = store.get_from_key(link, self.data["_id"])
        for i in range(len(elements)):
            _id = f'{store.get_name()}_{i}'
            self._add_link(link, _id, elements[i])
        return self

    def _add_link(self, link, _id, element):
        links = self.links[link] if link in self.links else {}
        links[_id] = element.get_description()
        self.links[link] = links

    def export(self, formatter):
        formatter.as_dict(self.data)
        formatter.as_dict(self.links)

class ListElementResult(DatastoreElement):
    def __init__(self, element: [], entity_name: str):
        super().__init__(list(element))
        self.entity_name = entity_name

    def export(self, formatter):
        formatter.as_line('---------------------------------------------------------------')
        formatter.as_line(f'Search {self.entity_name.title()} with:')
        formatter.as_list(self.data)