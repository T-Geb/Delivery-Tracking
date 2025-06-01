import csv
import os

import Hashtable

hash_table = Hashtable.Hashtable()


# a method to read the csv file and parse for loading into the hash table
    # Time Complexity: Big O -- O(n) due to the for loop implemented to parse through the csv file
def parse_package_data(hash_table):
    print("Parsing Package Data")  ##Debug
    # using csvreader to parse through the csv file
    with open('package_data.csv', 'r') as csv_package_file:
        csv_reader = csv.reader(csv_package_file, delimiter=',')
        next(csv_reader)
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

            status = "At the Hub"
                # we're passing the id_package as key and the rest of the package values as value to the hash table
                #we're calling a set_package function that is implemented in the hash table class.
            hash_table.insert(id_package, [address, city, state, zip_code, delivery_deadline, weight, special_notes, status])

if __name__ == "__main__":
    parse_package_data(hash_table)
    hash_table.print_table()
    print(os.getcwd())
