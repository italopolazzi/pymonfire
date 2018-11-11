# -*- coding: utf-8 -*-
from pymonfire import Pymonfire
from datetime import datetime, timezone, timedelta

NOT_PROCCESSED, PROCCESSED, TO_COLLECT = 'NOT_PROCCESSED', 'PROCCESSED', 'TO_COLLECT'


class SyncPMF:
    def __init__(self):
        self.mode_collect = 'COLLECT_USERS'
        self.collectUsers()
        self.mode_collect = 'COLLECT_USERS'
        self.collectQuestions()

    def collectUsers(self):
        print("PULANDO...")
        # self.myPMF = Pymonfire({'collect': True, 'collection': 'users'})
        # self.key1, self.op1, self.value1 = 'updatedAt', '<', datetime.now(
        #     timezone.utc) - timedelta(minutes=3)

        # self.mg_data = []
        # print("COLETANDO DOCUMENTOS BASEADO NA DATA DE ATUALIZAÇÃO SEGUINDO A REGRA...")
        # self.fb_data = self.getFirebaseDocsBasedOnDateOfUpdated()

        # print("PREPARANDO DADOS PARA O MONGODB...")
        # self.prepareMongoData()
        # print("INSERINDO DADOS COLETADOS NO MONGODB...")
        # self.result = self.insertMongoDBDocs(self.mg_data)
        # print('collected' if self.result else 'not collected')

        # print("PROCESSANDO DADOS NO NTLK...")
        # self.mg_new_data = self.proccessDataInNTLK()
        # print("SETANDO DADOS PROCESSADOS PARA SEREM ENVIADOS AO FIREBASE...")
        # self.fb_new_data = self.mg_new_data
        # self.setFirebaseProccessedData()

    def collectQuestions(self):
        self.mode_collect = 'COLLECT_QUESTIONS'
        self.myPMF = Pymonfire({'collect': True, 'collection': 'questions'})
        self.key1, self.op1, self.value1 = 'sender', '==', '0x7EfHXFXcVEPJ25clY9sC4Y1Bf2'
        self.key2, self.op2, self.value2 = 'status', '==', 1

        self.mg_data = False
        print("COLETANDO DOCUMENTOS BASEADO NO SENDER E STATUS SEGUINDO A REGRA...")
        self.fb_data = self.getFirebaseDocsBasedOnSenderAndStatus()

        print("PREPARANDO DADOS PARA O MONGODB...")
        self.prepareMongoData()
        # print("INSERINDO DADOS COLETADOS NO MONGODB...")
        # self.result = self.insertMongoDBDocs(self.mg_data)
        # print('collected' if self.result else 'not collected')

        # print("PROCESSANDO DADOS NO NTLK...")
        # self.mg_new_data = self.proccessDataInNTLK()
        # print("SETANDO DADOS PROCESSADOS PARA SEREM ENVIADOS AO FIREBASE...")
        # self.fb_new_data = self.mg_new_data
        # self.setFirebaseProccessedData()

    def getFirebaseDocsBasedOnDateOfUpdated(self):
        try:
            return self.myPMF.myFirebase.getWhere(self.key1, self.op1, self.value1)
        except Exception as err:
            print(type(err), err)

    def getFirebaseDocsBasedOnSenderAndStatus(self):
        try:
            return self.myPMF.myFirebase.getWhereAnd(self.key1, self.op1, self.value1, self.key2, self.op2, self.value2)
        except Exception as err:
            print(type(err), err)

    def setFirebaseProccessedData(self):
        for doc in self.fb_new_data:
            # REMOVE A CHAVE DO MONGO _id E USA DE REFERÊNCIA PARA ATUALIZAR O DOCUMENTO NO FIREBASE
            id = str(doc.pop('_id'))
            user_ref = self.myPMF.myFirebase.coll.document(id)
            user_ref.update(doc)

    def insertMongoDBDocs(self, data):
        return self.myPMF.myMongo.insertMany(self.mg_data)

    def updateMongoDBDocs(self, data):
        return self.myPMF.myMongo.updateMany(data)

    def prepareMongoData(self):
        for doc in self.fb_data:
            # TRANSFORMA A REFERÊNCIA DO FIREBASE EM UM OBJETO DICT
            temp = doc.to_dict()

            # PEGA O id DO DOCUMENTO NO FIREBASE E TRANSFORMA EM UMA _id USADA NO MONGO
            # ADICIONA ALTERA A TAG PARA NÃO PROCESSADO
            if (self.mode_collect == "COLLECT_USERS"):
                # aqui os dados do mongo são um array de usuário
                temp['_id'] = doc.id
                temp['pymonfire_tag'] = NOT_PROCCESSED
                # self.mg_data.append(temp)
            else:
                # aqui os dados do mongo são um dicionário de perguntas mapeadas pelo remetente
                print(temp)
                if (not self.mg_data):
                    self.mg_data = {
                        '_id': temp['sender'],
                        'questions': []
                    }
                    print('VAZIO', self.mg_data)
                self.mg_data['questions'].append(temp)
        print()
        print()
        print(self.mg_data)

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
        self.updateMongoDBDocs(result)
        return result
