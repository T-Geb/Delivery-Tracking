

class Package:

#Defining a Package constructor that will be passed to the hashtable as value.
#The constructor takes the package.csv fields plus other dynamic fields set to default values added to meet some package constraints
    def __init__(self,id_package, address, city, state , zip_code, delivery_deadline, weight, special_notes,
                 status = "At the Hub", start_time = None , delivery_time = None):
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
        self.start_time = start_time  # set default
        self.delivery_time = delivery_time #set default
        self.address_index = None # to be used to access the distance matrix
        self.truck_id = None  # to identify truck assignment to packages
        self.address_corrected = False   #setting flags to handle package 9's address update
        self.correction_time = None   #storing package 9's address correction time for report printing purpose

    #A method to allow printing of Package objects for display and debugging
    def __repr__(self):
        return (f" {self.id_package}, {self.address}, {self.city}, {self.state}, {self.zip_code},"
                f"{self.delivery_deadline}, {self.weight}, {self.special_notes}, {self.status},"  
                f"{self.start_time}, {self.delivery_time}, {self.address_index}, {self.truck_id},"
                f"{self.address_corrected, self.correction_time}")








