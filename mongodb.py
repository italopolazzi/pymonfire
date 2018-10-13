from pymongo import MongoClient

def mongodb(*args):
    client = MongoClient('mongodb://localhost:27017/')

    db = client.firebase
    col = db.users

    docs = col.find()

    return docs
