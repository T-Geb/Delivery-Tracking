

class Trucks:

    max_load = 16
    average_speed = 18
    drivers = 2

    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []   # to store a list of package objects
        self.total_miles = 0.0  # to keep track of the distance traveled

# a method to add packages to trucks. It makes sure that the max load of the truck, 16 is not exceeded
    def add_package(self, package):
        if len(self.packages) < Trucks.max_load:
            self.packages.append(package)
        else:
            print(f"Truck {self.truck_id} is full, cannot add package{package.id_package}")