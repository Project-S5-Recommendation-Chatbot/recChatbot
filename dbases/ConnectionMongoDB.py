import pymongo

class ConnectionMongoDB:
    def __init__(self, uri):
        self.uri = uri
        self.client = None

    def connect(self):
        self.client = pymongo.MongoClient(self.uri)
        return self.client

    def close(self):
        if self.client:
            self.client.close()