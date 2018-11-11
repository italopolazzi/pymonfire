# -*- coding: utf-8 -*-
from pymongo import MongoClient, errors


class MyMongo:
    def __init__(self, collection):
        self.client = MongoClient('mongodb://localhost:27017/')
        # BASE DE DADOS = firebase
        self.db = self.client.firebase
        self.setCollection(collection)

    def setCollection(self, collection):
        self.coll = self.db.get_collection(collection)

    def getDocs(self):
        return self.coll.find()

    def getWhere(self, params):
        return self.coll.find(params)

    def updateMany(self, data):
        for doc in data:
            self.coll.update_one({'_id': doc['_id']}, {'$set': doc})
        return True

    def insertOne(self, datum):
        try:
            self.coll.insert_one(datum)
            return True
        except errors.DuplicateKeyError as duplicated:
            print(type(duplicated), duplicated)
            return False
        except Exception as e:
            print(type(e), e)
            return False

    def insertMany(self, data):
        for doc in data:
            try:
                self.coll.insert_one(doc)
            except errors.DuplicateKeyError as duplicated:
                print(type(duplicated), duplicated)
                continue
            except Exception as e:
                print(type(e), e)
                return False
        return True
