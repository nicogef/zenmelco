# Zenmelco
For Zendesk Melbourne - Coding Challenge

Command line application to search data in json files and return the results in a human readable format.

# 
Language: Python

Command:
- Run test
 > python -m unittest discover -s tests -v
- Run program
 > python .\src\zenmelco.py
 
# Assumptions
1. All input files data are correctly formatted (No checks upon loading).
2. Out links are refers to a unique record
3. In links can be refered from multiple records
4. All date are in iso format
5. Boolean fields are Mandatory Fields