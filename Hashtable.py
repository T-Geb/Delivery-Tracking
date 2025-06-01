from importlib.metadata import packages_distributions
from operator import index

import Packages

class Hashtable:

    # creating the constructor for the hashtable with a size of 40 to take the 40 package values and assign each index with None.
    def __init__(self, size = 40):
        self.hash_list = [None] * size

# defining the hash function using the modulo operator
    def hash(self,key):
        my_hash = key % len(self.hash_list)

    ## print function to test the hash table is properly populated
    def print_table(self):
        for row in self.hash_list:
            print(row)

    def set_package(self, id_package, package):
        index = self.hash(id_package)   #calling the hash function to calculate an index using the id_package
        if self.hash_list[index] == None:   #if the bucket at index is empty, create an empty list at that index
            self.hash_list[index] = []
        #append the package key - id_package and value - package at the end of the list at index
        self.hash_list[index].append([package.id_package, package])

