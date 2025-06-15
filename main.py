# C950 Data Structures and Algorithms II  

import csv
from datetime import timedelta
from Hashtable import Hashtable
from Package import Package
from Trucks import Truck

hash_table = Hashtable() #initializing hashtable
address_dict = {}  # creating an empty dictionary list for storing addresses. Chose dictionary over list because of O(1) read and search
distance_matrix = [] #Defining Distance Matrix for distance lookup

# Time Complexity: O(n) due to the for loop implemented to parse through the csv file
# a method to read the csv file and parse for loading into the hash table by using key - package id and value - package object
def parse_package_data():
    # using csvreader to parse through the csv file
    with open('package_data.csv', 'r') as csv_package_file:
        csv_reader = csv.reader(csv_package_file, delimiter=',')
        next(csv_reader) # to make sure the first line containing headers is skipped
        for row in csv_reader: #for each row in the csv file, assign them to package objects
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

            # Passing the id_package as key and package object as value.
            # Calling an insert function that is implemented in the hash table class to add each key-value pair to hashtable
            hash_table.insert(id_package, package) # key - package ID, value = Package object

#Time Complexity: O(n) due to the for loop implemented to parse through the csv file
# parsing address.csv file to create the address_dict lookup table
def parse_address_data():
    with open('address.csv', 'r') as csv_package_file:
        csv_reader = csv.reader(csv_package_file, delimiter=',')
        for row in csv_reader:
            index = int(row[0]) # converting each first value of each row into an int that can be used as index
            address = row[2].strip()    # getting the address from the csv-located at index 2, and removing whitespace
            address_dict[address] = index # putting the address into the dictionary
            #this stores the address as Key and the index as value, because we want to look up by address to get the index for distance lookup

        return address_dict

#Time Complexity: O(n) due to the for loop implemented to parse through the csv file
#parsing distance.csv file and adding it to the distance_matrix
def parse_distance_data():
    with open('distance.csv', 'r') as csv_package_file:
        csv_reader = csv.reader(csv_package_file, delimiter=',')
        for row in csv_reader:
            distance_matrix.append(row)
    return distance_matrix

#Time Complexity: O(n) due to the for loop implemented to loop through the list of package id's
"""load_truck method looks up each package ID from the package id list by using the hashtable lookup method,
loads it onto the given truck's package list from truck class and sets package status by applying constraints"""
def load_truck(truck, list_package_ids):
    for pkg_id in list_package_ids:  # package_ids is a manually made list that contains the packages that should go on each truck
        package = hash_table.lookup(pkg_id) # looking up the package id in the hashtable and assigning it to a package variable.
        if package is not None:
            truck.add_package(package)## if found, then add the package to the truck's package list
            if package.id_package in (6, 25, 28, 32):  ## setting status for the delayed packages and for regular packages
                package.status = "Delayed"
            else:
                package.status = "At the hub" # package loaded at the hub
            package.truck_id = truck.truck_id

#Time Complexity: O(1)
"""A method to return a distance between two addresses by translating them to indices by using the address_dict and reading 
distance matrix"""
def get_distance(starting_address, ending_address):
    #address dict takes the address as key and returns the index as value
    start_index = address_dict[starting_address.strip()]
    end_index = address_dict[ending_address.strip()]
    #the distance matrix gives us the distance between addresses
    distance = distance_matrix[start_index][end_index]  #return the distance at those indices
    if distance == '':   #this checks if the distance is blank, to check the reverse location. Important since half of the distance matrix is blank
        distance = distance_matrix[end_index][start_index]  #checking the other side
    return float(distance)

#Time Complexity: O(1) - hashtable lookup
"""A method to update package 9's address at 10:20 am and also defines dynamic variables to flag package 9 as corrected
and to store the correction time for report generation"""
def update_package9_address(current_time):
    if current_time >= timedelta(hours=10,minutes=20):
        package_9 = hash_table.lookup(9)
        package_9.address = "410 S State St" # assigning correct address
        package_9.zip_code = "84111"
        package_9.special_notes = "Address Correction Made"  # replacing special note about wrong address
        #hashtable stores reference to the package object, so we can access these new additions from the hashtable.
        package_9.address_corrected = True  # to track if address 9 was corrected
        package_9.correction_time = current_time # storing correction time



#Algorithm: Nearest Neighbor
#Time Complexity: O(N^2) - due to the nested loops
"""The algorithm takes a truck start time, keeps a list of undelivered packages, repeatedly selects nearest address,
updates each package's status, delivery time, and the truck's mileage. 
The method returns the truck's arrival time back at the hub."""
def nearest_neighbor(truck,start_time = timedelta(hours=8)):
    undelivered_packages = list(truck.packages)  #create copy of the  list to track if a truck has any undelivered packages
    current_location = "4001 South 700 East"  #assign the starting location, the HUB
    current_time = start_time

    while undelivered_packages:   #while we still have undelivered packages:
        min_distance = float('inf')  # assigning min distance to infinity so the first package is immediately assigned minimum distance.
        nearest_package = None

        for package in undelivered_packages:  # finds the nearest package in each iteration
            distance = get_distance(current_location, package.address) # pass the package address to get the distance
            if distance < min_distance:     #if distance is less than min_distance then that package is assigned as the nearest
                #only update when we find something closer
                min_distance = distance
                nearest_package = package  #hashtable look up already done when loading trucks
        if nearest_package is not None:

            nearest_package.status = "En route"  # status update: package on the way

            #calculating travel time
            travel_time_minutes = (min_distance/truck.average_speed) * 60   #Calculate the distance in minutes based on the trucks speed - 18 mph
            travel_time = timedelta(minutes=travel_time_minutes)

            current_time += travel_time #updating current time

            nearest_package.delivery_time = current_time # setting package delivery time
            nearest_package.start_time = start_time # for status lookup

            truck.truck_miles += min_distance #saving truck miles
            truck.mileage_log.append((current_time,truck.truck_miles)) # to use for printing truck miles at a given query time

            # assigning the nearest location as the current location
            current_location = nearest_package.address

            #Removing the delivered package from the undelivered_list
            undelivered_packages.remove(nearest_package)

            #updating status once package is delivered
            nearest_package.status = "Delivered"

    distance_to_hub = get_distance(current_location, "4001 South 700 East") #calulating our return trip distance
    truck.truck_miles += distance_to_hub   #Tracking total miles traveled thus far.
    travel_time_hub = timedelta(minutes=((distance_to_hub/truck.average_speed) * 60) )
    current_time += travel_time_hub #adding travel_time_hub to the current time
    truck.mileage_log.append((current_time,truck.truck_miles))  # keeping a log of miles after each delivery to use for printing truck
                                                                # miles at a given query time
    truck.return_time = current_time # setting truck return time
    return current_time  #returning the time the truck finished delivering, to be used for truck assignment : truck 3

#Time Complexity: O(N^2) : due to the nearest_neighbor calls that are O(N^2)
"""Delivery Simulation that parses input files, create three trucks,assigns trucks, load them with pre-selected package-ID lists,
 and calls the nearest_neighbor routes while making sure constraints such as delayed flights and address correction at 10:20 am
are met"""
def run_delivery():

    #reading data csv files
    parse_package_data()
    parse_address_data()
    parse_distance_data()

    ##instantiating truck objects and assigning truck_id
    truck1 = Truck(truck_id=1)
    truck2 = Truck(truck_id=2)
    truck3 = Truck(truck_id=3)

    """Preparing a list of packages to load onto trucks. using manual method:
    Special notes were taken into account on which packages go together based same address, restrictions
    such as, can only be on truck 2 and the delayed on flight"""
    truck1_packages = [1, 4, 7, 8, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 39,
                       40]  # added normal packages + packages with earlier delivery deadline
    truck2_packages = [3, 5, 6, 18, 25, 26, 27, 31, 32, 35, 36, 37,
                       38]  # added normal packages + packages that can only go on truck 2 + delayed packages
    truck3_packages = [2, 9, 10, 11, 12, 17, 22, 23, 24, 28,
                       33]  # added normal packages + delayed on flight + package 9 - wrong address


    # Truck 1 starts at the default time 8:00am
    load_truck(truck1, truck1_packages)  # loading truck 1
    truck1_delivery = nearest_neighbor(truck1)  # running the nearest neighbor algorithm, truck 1 starting at default time 8:00 am


    # truck 2 starts at 09:05: waiting for the delayed packages to arrive at 9:05am
    truck2.start_time = timedelta(hours=9, minutes=5)
    load_truck(truck2, truck2_packages)  # loading truck 2
    nearest_neighbor(truck2,truck2.start_time) #run nearest_neighbor for truck 2

    # Truck 3 starts at >= 10:20am based on the given constraint for package 9 and truck 1's return time
    load_truck(truck3, truck3_packages) #loading truck 3
    # truck 3 waits until truck 1 returns...and until it's 10:20 so package 9 can get updated
    truck3.start_time = max(truck1_delivery, timedelta(hours=10, minutes=20))
    update_package9_address(truck3.start_time)  # calling a method to update package 9 at 10:20am
    nearest_neighbor(truck3, truck3.start_time) # run nearest_neighbor for truck 3

    # After truck 3 is done, all packages are expected to be delivered.

    return { #returning each truck object as a dictionary list to be used for the print function.
        "trucks_dict": {1: truck1, 2: truck2, 3: truck3}
    }

#Time Complexity - O(1) constant time lookups, comparisons and formatting
"""A method to display full report for one package at a given query time, including corrected address logic for package 9.
The report includes essential package information such as status, delivery time, truck ID, and more."""
def print_package_report(id_package, query_time):
    package = hash_table.lookup(id_package)
    display_address = package.address

    #Address display logic for package 9 : checks if correction_time is set.
    # and displays the original or corrected address accordingly
    if package.id_package == 9:
        if package.correction_time is None or query_time < package.correction_time: # The algorithm handles the package correction at 10:20
            display_address = "300 State St"  #showing original wrong address
        else:
            display_address = "410 S State St" # showing corrected address if the correction has happened

    # Package status logic: determine status based on package delivery_time and start_time
    # including special handling for delayed packages(IDs 6,25,28,32)
    if package.delivery_time is not None and query_time >= package.delivery_time:
        status= f"Delivered at {package.delivery_time}"
    elif (package.id_package in (6,25,28,32) and  #making sure the delayed packages are marked and shown as--
                                                  # --delayed by using the delivery's start time as a measure
          package.start_time is not None and
          query_time < package.start_time):
        status = "Delayed"
    elif package.start_time is not None and query_time < package.start_time:
        status = "At the Hub"
    else:
        status = "En route"

    # converting time objects to string for proper print display
    start_str = str(package.start_time)

    # Printing report. Uses formatting for proper display
    print(f"{package.id_package:<5} {display_address:<40} {package.city:<20} {package.state:<10}"
          f"{package.zip_code:<15} {package.weight:<10} {package.delivery_deadline:<20} {start_str:<20} {status:<30} "
          f"{package.truck_id:<6}  ")




#Time Complexity : O(n)
# method to return the total mileage a truck has traveled as of a specific query time
# uses a mileage log that is updated during the delivery algorithm
def get_truck_mileage(truck, query_time):
    latest_mileage = 0.0
    #since the log is added in time order, the for loop find the last mileage before the query time.
    for time, miles in truck.mileage_log:
        if time <= query_time:
            latest_mileage = miles
        else:
            break # to exit the loop once we find the latest time
    return latest_mileage


#Time Complexity: O(N) - due to the for to look up each package id and call to the report
"""A method to display report for all packages by looping through the package Id's 1-40 and calling the single package print
method to print reports.
The report also includes the total mileage traveled by all truck thus far"""
def print_all_report(query_time, truck_dict):
    print(f"\n--- Printing all package statuses at Query time: {query_time}")
    print(
        f"{'ID':<5} {'Address':<40} {'city':<20} {'State':<10}"
        f"{'Zip-Code':<15} {'Weight':<10} {'Deadline':<20} {'Departure Time':<20} {'Status':<30}"
        f"{'Truck':<6}  "
    )

    for id_package in range(1, 41): # for packages with id 1-40
        print_package_report(id_package, query_time) # call the package report method for each package

    #Calculate dynamic mileage as of query_time
    mile1 = get_truck_mileage(truck_dict[1], query_time)
    mile2 = get_truck_mileage(truck_dict[2], query_time)
    mile3 = get_truck_mileage(truck_dict[3], query_time)

    total_miles = mile1 + mile2 + mile3

    print(f"\n Total miles Traveled by all trucks as of {query_time} is {total_miles:.2f} miles.")



#Time Complexity O(1)
"""print report to display each truck's start time, when it returned to hub and truck miles
the trucks_dict passed from the run_delivery method is used to access the truck attributes"""
def print_truck_report(trucks_dict):

    print("\n================Truck Summary Report====================")
    print(f"\nTruck 1 started at: {trucks_dict[1].start_time} and returned to hub at : {trucks_dict[1].return_time}")
    print(f"Truck 1 Miles: {trucks_dict[1].truck_miles:.2f}")


    print(f"\nTruck 2 started at: {trucks_dict[2].start_time} and returned to hub at : {trucks_dict[2].return_time}")
    print(f"Truck 2 Miles: {trucks_dict[2].truck_miles:.2f}")

    print(f"\nTruck 3 started at: {trucks_dict[3].start_time} and returned to hub at : {trucks_dict[3].return_time}")
    print(f"Truck 3 Miles: {trucks_dict[3].truck_miles:.2f}")


    # Calculating total miles of all trucks
    total_miles = trucks_dict[1].truck_miles + trucks_dict[2].truck_miles + trucks_dict[3].truck_miles
    print(f"\nTotal miles traveled by all trucks is {total_miles:.2f} ")


if __name__ == "__main__":

    print("\n\n====================Delivery Tracking System======================")
    print("\n\nRunning Delivery Simulation")
    result = run_delivery()
    trucks = result["trucks_dict"]

    print("\n\n==============Simulation Complete===============")
    print("All packages delivered. You can now query status reports")
    print("Note: Please use 24-hour format for time entries E.g 10:20, 13:50, 20:00")
    print("\n\nPlease choose a report to view: Enter numbers only")
    print("\n1. View status report for all packages")
    print("\n2. View status report for a specific package at a specific time")
    print("\n3. View Truck Summary including total mileage")
    print("\n4. Enter 4 to exit the system\n")

    while True: # while loop to allow for dynamic display of menu   Time-Complexity - O(N)
        # taking user
        report_choice = input("\n\n\nEnter your choice:  \n\n\n").strip()

        if report_choice == "1":
            try:    #Using try and except to handle validation for proper time entry
                time_input = input("Please Enter time to view report in format HH:MM: ").strip()
                hours, minutes = map(int, time_input.split(":")) #splitting hours and minutes by the : delimiter

                #validation for proper time entry
                if not(0 <= hours <= 23 and  0 <= minutes <= 59):
                    print("\n\nINVALID INPUT: Hours must be 0-23 and minutes must be 0-59\n\n")
                    continue
                time_input = timedelta(hours=hours, minutes=minutes) # assigning the hours and minutes as timedelta to time_input
                print_all_report(time_input,trucks)  # calling all report printing method
            except ValueError: #Validation
                print("\n\nINVALID INPUT: Please use HH:MM format\n\n")
                continue

        elif report_choice == "2":
            try:  #Using try and except to handle validation for proper time entry
                package_id = int(input("Please Enter Package ID: 0-40").strip()) #converting package_id to integer for validation

                if not(0 <= package_id <= 40):  #validation for package ID range
                    print("\n\nINVALID INPUT: Package IDs must be 0-40\n\n")
                    continue

                time_input = input("Please Enter time to view report in format HH:MM:")
                hours, minutes = map(int, time_input.split(":"))

                if not(0 <= hours <= 23 and  0 <= minutes <= 59): # validation for time entry
                    print("\n\nINVALID INPUT: Hours must be 0-23 and minutes must be 0-59\n\n")
                    continue
                time_input = timedelta(hours=hours, minutes=minutes)

                print(  # print format
                    f"{'ID':<5} {'Address':<40} {'city':<20} {'State':<10}"
                    f"{'Zip-Code':<15} {'Weight':<10} {'Deadline':<20} {'Departure Time':<20} {'Status':<30} "
                    f"{'Truck':<6}  "
                )
                print_package_report(package_id, time_input) # calling single package report print method
            except ValueError:
                print("\n\n***INVALID INPUT: Please enter valid numbers***\n\n")
                continue
        elif report_choice == "3":
            print_truck_report(trucks)  # printing truck report to show delivery has successfully finished
        elif report_choice == "4":   # exit
            print("\nThank you for using the delivery tracking system")
            break
        else:
            print("\nINVALID CHOICE: Please try again. Enter 1 - to view all package reports, "
                  "2 - to view specific package report, or 3 - to exit the system\n")































