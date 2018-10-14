from pymonfire import Pymonfire
from datetime import datetime, timezone, timedelta
import bson
import json
class SyncPMF:
    def __init__(self):
        self.myPMF = Pymonfire({})
        self.key, self.op, self.value = 'updatedAt', '<', datetime.now(
            timezone.utc) - timedelta(minutes=3)

        self.fb_data = self.getFirebaseDocsBasedOnDateOfUpdated()
        self.mg_data = []
        self.sync()
        self.result = self.udateMongoDBDocsBasedOnDateOfUpdate()

        print('collected' if self.result else 'not collected')

    def getFirebaseDocsBasedOnDateOfUpdated(self):
        try:
            return self.myPMF.myFirebase.getWhere(self.key, self.op, self.value)
        except Exception as err:
            print(type(err), err)

    def udateMongoDBDocsBasedOnDateOfUpdate(self):
        return self.myPMF.myMongo.insertMany(self.mg_data)

    def sync(self):
        for doc in self.fb_data:
            temp = doc.to_dict()
            temp['_id'] = doc.id
            temp['proccessed'] = False
            self.mg_data.append(temp)
            # print(self.mg_data)




v = SyncPMF()
