from datetime import timedelta


class Truck:
# A truck class to keep store truck data
    max_load = 16   # a truck can hold upto 16 packages
    average_speed = 18  # truck has average speed of 18mph

    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []   # to store a list of package objects
        self.truck_miles = 0.0  # to keep track of the distance traveled
        self.start_time = timedelta(hours=8) # default time : for managing truck's start time
        self.return_time = None  #initially set to 0.

    #Time-Complexity:  O(1) - appending
    # a method to add package to truck if truck's max_load, 16 is not exceeded
    def add_package(self, package):
        if len(self.packages) < Truck.max_load:
            self.packages.append(package)

