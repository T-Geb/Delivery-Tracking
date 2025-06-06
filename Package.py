


class Package:

#Defining a Package constructor that will be passed to the hashtable as value.
#The constructor takes the package.csv fields plus three dynamic fields set to default values for status, departure_time and
#delivery_time
    def __init__(self,id_package, address, city, state , zip_code, delivery_deadline, weight, special_notes,
                 status = "At the Hub", departure_time = None, delivery_time = None):
        #saving the parameters into the object as attributes
        self.id_package = id_package
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = status
        self.departure_time = departure_time
        self.delivery_time = delivery_time
        self.address_index = None # to be used to access the distance matrix

    #Debug:: adding a method to allow printing of object contents for Debugging purposes
    def __repr__(self):
        return (f" {self.id_package}, {self.address}, {self.city}, {self.state}, {self.zip_code},"
                f"{self.delivery_deadline}, {self.weight}, {self.special_notes}, {self.status}," 
                f"{self.departure_time}, {self.delivery_time}")








