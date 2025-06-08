import csv
from datetime import datetime, timedelta
from importlib.metadata import packages_distributions
from xml.sax import default_parser_list

from Hashtable import Hashtable
from Package import Package
from Trucks import Trucks

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
            hash_table.insert(id_package, package) # key - package ID, value = Package object
# Pre-algorithm steps:

address_dict = {}  # creating an empty dictionary list for storing addresses. Chose dictionary over list because of O(1) read and search
# parsing address.csv file to create the address_dict lookup table
def parse_address_data(address_dict):
    with open('address.csv', 'r') as csv_package_file:
        csv_reader = csv.reader(csv_package_file, delimiter=',')
        for row in csv_reader:
            index = int(row[0]) # converting each first value of each row into an int that can be used as index
            address = row[2].strip()    # getting the address from the csv and removing whitespace
            address_dict[address] = index # putting the address into the dictionary
            #this stores the address as Key and the index as value, because we want to look up by address to get the index

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

# a method to load truck
def load_truck(truck, hash_table, list_package_ids):
    for package_id in list_package_ids:  #package_ids is a manually made list that contains the packages that should go on each truck
        package = hash_table.lookup(package_id) # looking up the package id in the hashtable and assigning it to package object
        if package is not None:
            truck.add_package(package)## if found, then add the package to the truck
            package.status = "At the hub" # package loaded at the hub
            package.truck_id = truck.truck_id
            # print(f"Loaded package {package_id} onto truck {truck.truck_id}")
        # else:
            # print(f" Package {package_id} not found") # if no package exists

def get_distance(starting_address, ending_address):
    #address dict takes the address as key and returns the index as value
    start_index = address_dict[starting_address.strip()]
    end_index = address_dict[ending_address.strip()]
    #the distance matrix gives us the distance between addresses
    distance = distance_matrix[start_index][end_index]  #return the distance at those indices
    if distance == '':   #this checks if the distance is blank, to check the reverse location. Important since half of the distance matrix is blank
        distance = distance_matrix[end_index][start_index]  #checking the other side
    return float(distance)

def nearest_neighbor(truck,start_time = timedelta(hours=8)):
    undelivered_packages = list(truck.packages)  #create a list to track if a truck has any undelivered packages
    current_location = "4001 South 700 East"  #assign the starting location, the HUB
    # print(f"Current location: {current_location}")  ##DEBUG
    current_time = start_time
    print(f" Truck {truck} Current time: {current_time}")
    while undelivered_packages:   #while we still have undelivered packages:
        min_distance = float('inf')  # assigning min distance to infinity so the first package is immediately assigned minimum distance.
        nearest_package = None
        for package in undelivered_packages:  # finds the nearest package in each iteration
            distance = get_distance(current_location, package.address) # pass the package address to get the distance
            if distance < min_distance:     #if distance is less than min_distance then that package is assigned as the nearest
                #only update when we find something closer
                min_distance = distance
                nearest_package = package
                print(f"Distance: {min_distance}") #DEBUG print
        if nearest_package is not None:

            nearest_package.status = "En route"  # package on the way

            #calculating travel time
            travel_time_minutes = (min_distance/18.0) * 60   #Calculate the distance in minutes based on the trucks speed - 18 mph
            travel_time = timedelta(minutes=travel_time_minutes)

            current_time += travel_time #updating current time

            nearest_package.delivery_time = current_time # setting package delivery time
            nearest_package.start_time = start_time # for status lookup

            truck.total_miles += min_distance

            # moving the current location indicator to the nearest address we're working with
            current_location = nearest_package.address
            # print(f"Current location after delivering: {current_location}") #Debug Print

            #Removing the delivered package from the undelivered_list
            undelivered_packages.remove(nearest_package) # do i need a remove method?

            #updating status:
            nearest_package.status = "Delivered"
            # print(f"Delivered Package {nearest_package.id_package} at {current_time}")#Debug print

    distance_to_hub = get_distance(current_location, "4001 South 700 East") #calulating our return trip distance
    print(f"Distance to hub: {distance_to_hub}")
    truck.total_miles += distance_to_hub   #Tracking total miles traveled thus far.
    print(f"Total miles: {truck.total_miles}")
    # travel_time_minutes =   #recalculating travel minutes to include travel to hub
    travel_time_hub = timedelta(minutes=((distance_to_hub/18.0) * 60) )
    current_time += travel_time_hub# adding travel_time_hub to the current time
    print(f"Current time After Delivery of {truck.truck_id} {current_time}")
    # print(f"Returned to HUB at {current_time}")
    return current_time
# method to update package 9 address:

# def delayed_addresses(package_id):
#     if package_id == 6 or package_id == 25 or package_id == 28 or package_id == 32:
#         if package.delivery_time is not None and


def update_package9_address(current_time, hash_table):
    if current_time >= timedelta(hours=10,minutes=20):
        package_9 = hash_table.lookup(9)
        package_9.address = "410 S State St" # assigning correct address
        package_9.zip_code = "84111"
        package_9.special_notes = "Address Correction Made"  # replacing special note about wrong address
        print(f"Updating Package 9: {package_9}")
        print(f"Package 9 : Current time: {current_time}")
    return package_9.id_package

def print_package_status(id_package, query_time):
    package = hash_table.lookup(id_package)
    # print(f"Debug - Package {package.id_package}")
    # print(f"Debug - Query time: {query_time}")
    # print(f"Debug - delivery_time: {package.delivery_time}")
    # print(f"Debug - start_time: {package.start_time}")

    if package.delivery_time is not None and query_time >= package.delivery_time:
        status = f"Delivered at {package.delivery_time}"
    elif package.start_time is not None and query_time < package.start_time:
        status = "At the Hub"
    else:
        status = "En route"
    print(f" Package Status:  {id_package} Status: {status}")
    print(f" Truck ID: for Package {package.id_package} is {package.truck_id}")


def print_all_status(query_time):
    print(f"\n--- Printing all package statuses at Query time: {query_time}")
    for id_package in range(1, 41):
        package_status = hash_table.lookup(id_package)
        print_package_status(package_status.id_package, query_time)



if __name__ == "__main__":
    parse_package_data(hash_table)
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
    # printing_addresses(address_dict)   # DEBUG : printing added addresses
    parse_distance_data(distance_matrix)
    # print_distance_data(distance_matrix)

    ##loading trucks:
    truck1 = Trucks(truck_id=1)
    truck2 = Trucks(truck_id=2)
    truck3 = Trucks(truck_id=3)

    #assigning some packages as Delayed
    hash_table.lookup(6).status = "Delayed"
    hash_table.lookup(25).status = "Delayed"
    hash_table.lookup(28).status = "Delayed"
    hash_table.lookup(32).status = "Delayed"

    # # updating package 9's address before loading it to truck
    update_package9_address(timedelta(hours=10, minutes=20), hash_table)  # updated package 9 address
    hash_table.lookup(9)
    print(f"Package 9: {hash_table.lookup(9)}")


#Preparing a list of packages to load onto trucks. using manual method:
#manually loaded each truck...Special notes were taken into account on which packages go together based same address, restrictions
    #--such as can only be on truck 2 and the delayed on flight were added to truck 3
    truck1_packages = [1,4,7,8,13,14,15,16,19,20,21,29,30,34,39,40] # added normal packages + ones that need to go together
    truck2_packages = [3,5,6,18,25,26,31,32,36,37,38] # added normal packages + packages that can only go on truck 2
    truck3_packages = [2,9,10,11,12,17,22,23,24,27,28,33,35]  # added normal packages + ones that go together + delayed on flight + package 9 - wrong address

#using a method to load the packages onto the trucks
    load_truck(truck1, hash_table,truck1_packages)

    #truck 2 starts at 10:20am: waiting for package 9 address to be updated and the delayed packages arriving at 9:05am
    truck2.start_time = timedelta(hours=9, minutes=5)
    load_truck(truck2, hash_table, truck2_packages)

    truck1_delivery = nearest_neighbor(truck1) # take default start time 8:00am
    truck2_delivery = nearest_neighbor(truck2,truck2.start_time) # take start time 9:05am to account for delayed packages
    print("Truck 1 Delivery ", truck1_delivery)
    print("Truck 2 Delivery ", truck2_delivery)

    # truck 3 waits until truck 1 returns...and until it's 10:20 so package 9 can get updated
    truck3.start_time = truck1_delivery
    if truck3.start_time < timedelta(hours=10,minutes=20):
        truck3.status = timedelta(hours=10, minutes=20)

    load_truck(truck3, hash_table, truck3_packages)
    truck3_delivery = nearest_neighbor(truck3,truck3.start_time )
    print("Truck 3 Delivery ", truck3_delivery)

    print(f"\n--- Package Status at Query time: timedelta(hours=10, minutes=15")
    print_package_status(6, timedelta(hours=10, minutes=15))

    total_miles = truck1.total_miles + truck2.total_miles + truck3.total_miles
    print(f"Total miles: {total_miles}")
    # package_28 = hash_table.lookup(28)
    #
    # print(f"Package 28 : {package_28}")
    # print(f"Pkg 28 delivery time: {package_28.delivery_time}")


    print_all_status(timedelta(hours=8, minutes=50))
    print_all_status(timedelta(hours=9, minutes=40))
    print_all_status(timedelta(hours=13, minutes=5)) #24-hour format 1:05


















