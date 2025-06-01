
import csv

class Packages:

    def __init__(self,id_package, address, city, state , zip_code, delivery_deadline, weight, special_notes):
        #saving the parameters into the object as attributes
        self.id_package = id_package
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes

    # a method to read the csv file and parse for loading into the hash table
    def parse_package_data(self, hash_table):
        with open('package_data.csv', 'r') as csv_package_file:
            csv_reader = csv.reader(csv_package_file, delimiter=',')
            for row in csv_reader:
                package = Packages(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                # we're passing the id_package as key and the whole package including the id_package as value to the hash table
                #we're calling a set_package function that is implemented in the hash table class.
                hash_table.set_package(package.id_package, package)




