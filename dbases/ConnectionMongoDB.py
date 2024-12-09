import pymongo  # Import the pymongo library for interacting with MongoDB

# Define a class to manage the MongoDB connection
class ConnectionMongoDB:
    def __init__(self, uri):
        """
        Initialize the ConnectionMongoDB object with the provided MongoDB URI.
        :param uri: MongoDB connection URI
        """
        self.uri = uri  # Store the MongoDB URI
        self.client = None  # Placeholder for the MongoDB client connection object

    def connect(self):
        """
        Establish a connection to the MongoDB server using the provided URI.
        :return: A MongoClient object representing the connection
        """
        self.client = pymongo.MongoClient(self.uri)  # Create a MongoDB client instance
        return self.client  # Return the client for further use

    def close(self):
        """
        Close the connection to the MongoDB server if it is currently open.
        """
        if self.client:  # Check if the client is connected
            self.client.close()  # Close the connection
