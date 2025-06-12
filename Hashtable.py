


class Hashtable:

    # Creating the constructor for the hashtable with a size of 59 to store the 40 packages
    # Hashtable size = 59, a prime number for good hash and to keep the load factor <= 0.7 if more packages are added
    def __init__(self, size = 59):
        self.hash_list = [None] * size

   # defining the hash function using the modulo operator
    def hash(self,key):
        return key % len(self.hash_list)

    #Time Complexity: Average Case - O(1), Worse Case - O(N) : if many collisions occur
    """The insert uses inputs key-value pairs to find the bucket index and create a list "
     at that bucket if the bucket is empty for linear probing"""
    def insert(self, key, value):
        index = self.hash(key)   #calling the hash function to calculate an index using the id_package
        bucket = self.hash_list[index]
        if bucket is None:   #if the bucket at index is empty, create an empty list at that index #this is for separate chaining. If two package objects map to the same index, the value gets appended to the list.
            bucket = []    #creating a new list
            self.hash_list[index] = bucket  # connecting the hashtable to the new list
        # append the package key - id_package and value - package at the end of the list at index
        # we don't need to pass the whole package value..that is done in main method..
        bucket.append([key, value])    # inserting the key value pair at the bucket


    #Time Complexity: Average Case - O(1), Worst Case - O(N) : if many collisions occur
    # The lookup method takes a package id as input to use as key and returns the values, package objects
    def lookup(self, key):
        index = self.hash(key)  # calling hash method to calculate the bucket index using the hash function
        bucket = self.hash_list[index]  # grabbing the bucket at that index

        if bucket is None:  # if bucket at that index is empty, return None
            return None
        for pair in bucket: # for the items in the bucket, key & Value
            # print("Checking pair:", pair)
            if pair[0] == key:   # if key at index 0 is equal to the key passed,
                # print("Matched")
                return pair[1]   # return the value that is at index 1
        return None











