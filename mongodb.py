from pymongo import MongoClient


class MyMongo:
    def __init__(self, collection):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.firebase
        self.coll = self.db.get_collection(collection)

    def getDocs(self):
        return self.coll.find()
