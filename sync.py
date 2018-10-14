from pymonfire import Pymonfire
from datetime import datetime, timezone, timedelta


class SyncPMF:
    def __init__(self):
        self.myPMF = Pymonfire({})

    # def getFirebaseDocsBasedOnDateOfUpdated(self):
    #     return self.myPMF.myFirebase.coll.where('user', '==', '').get()
    def getFirebaseDocsBasedOnDateOfUpdated(self, params):
        try:
            return self.myPMF.myFirebase.getWhere(params['key'], params['op'], params['value'])
        except Exception as err:
            print(type(err), err)


sync = SyncPMF()
past3days = datetime.now(timezone.utc) - timedelta(days=3)

for doc in sync.getFirebaseDocsBasedOnDateOfUpdated({
    'key': 'updatedAt',
    'op': '<',
    'value': past3days
}):
    print(doc.to_dict())

# print('inserted' if (pmf.insertOne(data2)) else 'not inserted')

# print('updated' if (pmf.updateOne(document_to_update())) else 'not updated')

# db.collection(u'data').document(u'one').set(data)
