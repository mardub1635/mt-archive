#!/usr/bin/env python3
"""
required package: nameparser

This script takes as an input a string containing a list of names 
and outputs the list of names with in the form "Last name, First name [Middle name]"
It can be called as a function. (from invert_name import invert_name)


Example usage (command line):

python invert_name.py 'John B. Smith and Pablo Ramirez-Gonzalez and Bob Doe'
>>>Smith, John B. and Ramirez-Gonzalez, Pablo and Doe, Bob



Author: Marie Dubremetz
"""

from nameparser import HumanName #'pip install nameparser' if import error occures
import sys

def invert_name(line):
	"""(String)->String
		
		given a string containing names separated by " and " returns the names with first name last name reverted
		
		>>>'John B. Smith and Pablo Ramirez-Gonzalez and Bob Doe'
		'Smith, John B. and Ramirez-Gonzalez, Pablo and Doe, Bob'
		"""
    line=line.replace(" And ", " and ")
    name_list=line.split(' and ')
    authors_list=[]
    for name in name_list:
        author = HumanName(name)
        author = author.last+", "+author.first+" "+author.middle
        author = author.strip()
        authors_list += [author]
    return " and ".join(authors_list)

if __name__ == "__invert_name__":
    line=sys.argv[1]
    invert_name(line)
    print(invert_name(line))