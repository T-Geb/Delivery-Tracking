from datetime import timedelta


class Trucks:

    max_load = 16
    average_speed = 18
    drivers = 2

    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []   # to store a list of package objects
        self.total_miles = 0.0  # to keep track of the distance traveled
        self.start_time = timedelta(hours=8) # default time : for managing truck's start time
        self.return_time = 0.0

    def add_package(self, package):
        if len(self.packages) < Trucks.max_load:
            self.packages.append(package)
        else:
            print(f"Truck {self.truck_id} is full, cannot add package{package.id_package}")

