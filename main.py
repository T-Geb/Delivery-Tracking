import csv

from Hashtable import Hashtable
from Package import Package

hash_table = Hashtable()


# a method to read the csv file and parse for loading into the hash table
    # Time Complexity: Big O -- O(n) due to the for loop implemented to parse through the csv file
def parse_package_data(hash_table):
    #print("Parsing Package Data")  ##Debug
    # using csvreader to parse through the csv file
    with open('package_data.csv', 'r') as csv_package_file:
        csv_reader = csv.reader(csv_package_file, delimiter=',')
        next(csv_reader) # to make sure the first line containing headers is skipped
        for row in csv_reader:
            ##editing for rubric requirement of no class usage:
            id_package = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            delivery_deadline = row[5]
            weight = row[6]
            special_notes = row[7]

            # passing the parsed data into the package object as attributes
            package = Package(id_package, address, city, state, zip_code, delivery_deadline, weight,special_notes)

                # we're passing the id_package as key and package object as value.
                #we're calling an insert function that is implemented in the hash table class.
            hash_table.insert(id_package, package)
# Pre-algorithm steps:

address_dict = {}  # creating an empty dictionary list for storing addresses. Chose dictionary over list because of O(1) read and search

def parse_address_data(address_dict):
    with open('address.csv', 'r') as csv_package_file:
        csv_reader = csv.reader(csv_package_file, delimiter=',')
        for row in csv_reader:
            index = int(row[0]) # converting each first value of each row into an int that can be used as index
            address = row[2].strip()    # assigning address index to dict by stripping whitespaces
            address_dict[address] = index

        return address_dict

#DEBUG method to check proper address dictionary population
def printing_addresses(address_dict):
    for address, index in address_dict.items():
        print(f"Index {index}: {address}")

#Defining Distance Matrix
distance_matrix = []
def parse_distance_data(distance_data):
    with open('distance.csv', 'r') as csv_package_file:
        csv_reader = csv.reader(csv_package_file, delimiter=',')
        for row in csv_reader:
            distance_matrix.append(row)
    return distance_matrix

def print_distance_data(distance_matrix):      #DEBUGGING Print method to check Distance Matrix population
    for index, distance in enumerate(distance_matrix):
        print(f"Distance {index}: {distance}")

if __name__ == "__main__":
    # parse_package_data(hash_table)
    # hash_table.print_table()
    #
    # # print(os.getcwd())
    # result = hash_table.lookup(39)  #add in check..if key not found...
    # if result:
    #     print("Lookup worked!")
    # else:
    #     print("Lookup failed.")
## DEBUT for address list:
    parse_address_data(address_dict)  #
    printing_addresses(address_dict)   # DEBUG : printing added addresses
    parse_distance_data(distance_matrix)
    print_distance_data(distance_matrix)






