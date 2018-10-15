from pymonfire import Pymonfire
from datetime import datetime, timezone, timedelta
from firebase_admin import firestore
import bson
import json

NOT_PROCCESSED, PROCCESSED, TO_COLLECT = 'NOT_PROCCESSED', 'PROCCESSED', 'TO_COLLECT'

class SyncPMF:
    def __init__(self):
        self.myPMF = Pymonfire({})
        self.key, self.op, self.value = 'updatedAt', '<', datetime.now(
            timezone.utc) - timedelta(minutes=3)

        self.mg_data = []
        self.fb_data = self.getFirebaseDocsBasedOnDateOfUpdated()
        
        self.prepareMongoData()
        self.result = self.udateMongoDBDocsBasedOnDateOfUpdate()
        print('collected' if self.result else 'not collected')

        self.fb_new_data = self.proccessDataInNTLK()
        self.setFirebaseProccessedData()

    def getFirebaseDocsBasedOnDateOfUpdated(self):
        try:
            return self.myPMF.myFirebase.getWhere(self.key, self.op, self.value)
        except Exception as err:
            print(type(err), err)

    def setFirebaseProccessedData(self):
        for doc in self.fb_new_data:
            # REMOVE A CHAVE DO MONGO _id E USA DE REFERÊNCIA PARA ATUALIZAR O DOCUMENTO NO FIREBASE
            id = str(doc.pop('_id'))
            user_ref = self.myPMF.myFirebase.coll.document(id)
            user_ref.update(doc)

    def udateMongoDBDocsBasedOnDateOfUpdate(self):
        return self.myPMF.myMongo.insertMany(self.mg_data)

    def prepareMongoData(self):
        for doc in self.fb_data:
            # TRANSFORMA A REFERÊNCIA DO FIREBASE EM UM OBJETO DICT
            temp = doc.to_dict()
            # PEGA O id DO USUÁRIO NO FIREBASE E TRANSFORMA EM UMA _id USADA NO MONGO
            temp['_id'] = doc.id
            # ADICIONA ALTERA A TAG PARA NÃO PROCESSADO
            temp['pymonfire_tag'] = NOT_PROCCESSED
            self.mg_data.append(temp)
    
    def proccessDataInNTLK(self):
        temp = self.myPMF.mgGetWhere({'pymonfire_tag': NOT_PROCCESSED})
        # **************************************************************************
        # FAZER O PROCESSAMENTO COM O NTLK AQUI
        # simulando que os dados foram processados
        # **************************************************************************
        result = []
        for doc in temp:
            doc['pymonfire_tag'] = PROCCESSED
            doc['updatedAt'] = datetime.now(timezone.utc)
            result.append(doc)
        return result




v = SyncPMF()
