# Zenmelco
For Zendesk Melbourne - Coding Challenge

Command line application to search data in json files and return the results in a human readable format.

# 
Language: [Python 3.7.9](https://www.python.org/downloads/release/python-379/)

Usage Instruction (from the root folder):
- Tests
 > python -m unittest discover -s tests -v
- Run program
 > python .\src\zenmelco.py

# Assumptions
1. All input files data are correctly formatted (No checks upon loading).
2. Out links refers to a unique record
3. In links can be refered from multiple records
4. All dates are in iso format

# Design
- tests
- src
  - zenmelco.py - Initialise the Datastore and start the UI
  - main_context.py - Manage the Program context and error level Exceptions
  - user_interface
    - menus.py - Contains the all the menus
    - menu_context.py - Manage the Menu context and Warning level Exeption
  - store
    - datastore_context.py - Defines the contract with the UI
    - datastore.py - Implements the datastore context and get the result from the store Entities
    - datastore_load.py - Loads the json files and initialise the entities
    - datastore_strategies - Defines indexing strategies
    - datastore_configuration - Maps the json file data to an indexing strategy (typed), defines keys for the links and other parameters
