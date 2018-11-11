# -*- coding: utf-8 -*-
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class MyFirebase:
    def __init__(self, collection):
        self.cred = credentials.Certificate('./src/json/keys.json')
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.setCollection(collection)

    def setCollection(self, collection):
        self.coll = self.db.collection(collection)

    def getDocs(self):
        return self.coll.get()

    def getWhere(self, k, o, v):
        return self.coll.where(k, o, v).get()

    def getWhereAnd(self, k1, o1, v1, k2, o2, v2):
        return self.coll.where(k1, o1, v1).where(k2, o2, v2).get()

    def updateOne(self, id, data):
        return self.coll.document(id).update(data)
