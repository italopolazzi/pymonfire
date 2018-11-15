# -*- coding: utf-8 -*-
from pymonfire import Pymonfire
from datetime import datetime, timezone, timedelta
from proccessor import Proccessor

NOT_PROCCESSED, PROCCESSED, TO_COLLECT = 'NOT_PROCCESSED', 'PROCCESSED', 'TO_COLLECT'


class SyncPMF:
    def __init__(self):
        self.collectUsers()

    def collectUsers(self):
        self.mode_collect = 'COLLECT_USERS'

        self.myPMF = Pymonfire()
        self.key1, self.op1, self.value1 = 'updatedAt', '<', datetime.now(
            timezone.utc) - timedelta(minutes=1)

        self.mg_data_users = []
        print("COLETANDO DOCUMENTOS BASEADO NA DATA DE ATUALIZAÇÃO SEGUINDO A REGRA...")
        self.fb_data = self.getFirebaseDocsBasedOnDateOfUpdated()

        print("PREPARANDO DADOS PARA O MONGODB...")
        self.prepareMongoData()
        print("INSERINDO USUÁRIOS COLETADOS NO MONGODB...")
        self.result = self.insertMongoDBUsers(self.mg_data_users)
        res_msg = 'users collected'
        print(res_msg if self.result else 'NOT! {}'.format(res_msg))

        if(self.result):
            self.mode_collect = 'COLLECT_QUESTIONS'
            print("DEFININDO A COLEÇÃO DO FIREBASE COMO QUESTIONS...")
            self.myPMF.fbSetCollection('questions')

            print("PERCORRENDO USUÁRIOS NÃO PROCESSADOS SALVOS NO MONGODB...")
            users_ids = self.getNotProccessedUsersIds()
            # SETA O MONGODB DO PYMONFIRE PARA ARMAZENAR EM QUESTIONS
            self.myPMF.mgSetCollection('questions')
            for user_id in users_ids:
                self.collectQuestions(user_id)

            print("PERGUNTAS DE TODOS USUÁRIOS NÃO PROCESSADOS COLETADAS...")

            print("PROCESSANDO DADOS NO NTLK...")
            self.mg_new_data = self.proccessDataInNTLK()
            print("SETANDO DADOS PROCESSADOS PARA SEREM ENVIADOS AO FIREBASE...")
            self.fb_new_data = self.mg_new_data
            self.setFirebaseProccessedData()

    def getNotProccessedUsersIds(self):
        temp = []
        users_not_proccessed = self.myPMF.mgGetWhere(
            {'pymonfire_tag': NOT_PROCCESSED})
        for user in users_not_proccessed:
            temp.append(user['_id'])
        return temp

    def collectQuestions(self, sender):
        self.key1, self.op1, self.value1 = 'sender', '==', sender
        self.key2, self.op2, self.value2 = 'status', '==', 1

        self.mg_data_questions = False
        print("COLETANDO DOCUMENTOS BASEADO NO SENDER E STATUS SEGUINDO A REGRA...")
        self.fb_data = self.getFirebaseDocsBasedOnSenderAndStatus()

        print("PREPARANDO DADOS PARA O MONGODB...")
        self.prepareMongoData(sender)
        print(self.mg_data_questions)
        print("INSERINDO PERGUNTAS COLETADAS NO MONGODB...")
        self.result = self.insertMongoDBQuestions(
            self.mg_data_questions) if self.mg_data_questions else False
        res_msg = 'questions for {} collected'.format(sender)
        print(res_msg if self.result else 'NOT! {}'.format(res_msg))

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
        # SETA O FIREBASE DO PYMONFIRE PARA ENVIAR PARA USUÁRIOS
        self.myPMF.fbSetCollection('users')
        for doc in self.fb_new_data:
            # REMOVE A CHAVE DO MONGO _id E USA DE REFERÊNCIA PARA ATUALIZAR O DOCUMENTO NO FIREBASE
            id = str(doc.pop('_id'))
            user_ref = self.myPMF.myFirebase.coll.document(id)
            user_ref.update(doc)
            # user_ref.set(doc)

    def insertMongoDBUsers(self, data):
        return self.myPMF.myMongo.insertMany(self.mg_data_users)

    def insertMongoDBQuestions(self, data):
        return self.myPMF.myMongo.insertOne(self.mg_data_questions)

    def updateMongoDBDocs(self, data):
        return self.myPMF.myMongo.updateMany(data)

    def prepareMongoData(self, sender=False):
        for doc in self.fb_data:
            # TRANSFORMA A REFERÊNCIA DO FIREBASE EM UM OBJETO DICT
            temp = doc.to_dict()

            # PEGA O id DO DOCUMENTO NO FIREBASE E TRANSFORMA EM UMA _id USADA NO MONGO
            # ADICIONA ALTERA A TAG PARA NÃO PROCESSADO
            if (not sender):
                # aqui os dados do mongo são um array de usuário
                temp['_id'] = doc.id
                temp['pymonfire_tag'] = NOT_PROCCESSED
                self.mg_data_users.append(temp)
            else:
                # aqui os dados do mongo são um dicionário de perguntas mapeadas pelo remetente
                if (not self.mg_data_questions):
                    self.mg_data_questions = {
                        '_id': sender,
                        'questions': []
                    }
                self.mg_data_questions['questions'].append(temp)

    def proccessDataInNTLK(self):
        # SETA O MONGODB DO PYMONFIRE PARA COLETAR DE USUÁRIOS
        self.myPMF.mgSetCollection('users')
        users = self.myPMF.mgGetWhere({'pymonfire_tag': NOT_PROCCESSED})
        # **************************************************************************
        # FAZER O PROCESSAMENTO COM O NTLK AQUI
        # simulando que os dados foram processados
        # **************************************************************************
        self.procc = Proccessor()
        result = []
        for user in users:
            user['my_tags'] = self.getUserQuestionsAndProccess(user)
            user['pymonfire_tag'] = PROCCESSED
            user['updatedAt'] = datetime.now(timezone.utc)
            result.append(user)
        # **************************************************************************
        # SALVA OS DADOS DO USUÁRIO ATUALIZADOS
        # mas ignora o salvamento das questions
        # **************************************************************************
        self.updateMongoDBDocs(result)
        return result

    def getUserQuestionsAndProccess(self, user):
        # SETA O MONGODB DO PYMONFIRE PARA COLETAR DE QUESTIONS
        self.myPMF.mgSetCollection('questions')
        # COLETA OS AS PERGUNTAS NO BUCKET DO USUÁRIO ATUAL
        cursor = self.myPMF.mgGetWhere({'_id': user['_id']})
        user_questions_bucket = None
        for item in cursor:
            user_questions_bucket = item['questions']
        print(user, ' => ', user_questions_bucket)
        # CONTA AS TAGS (PALAVRAS) QUANTAS VEZES ELAS APARECEM EM TODAS AS RESPOSTAS
        tags_counted = self.countTags(user_questions_bucket)
        # SELECIONA AS TAGS MAIS RELEVANTES BASEADAS NAS QUE APARECEM MAIS VEZES
        relevant_tags = self.getRelevantTags(tags_counted)
        return relevant_tags

    def countTags(self, questions):
        countTags = {}
        for question in questions:
            answer = question['answer']['text']
            # question = question.text
            tags = self.procc.proccess_one(answer)['autoTag']
            for tag in tags:
                if(tag in countTags):
                    countTags[tag] += 1
                else:
                    countTags[tag] = 1
        print('countTags => ', countTags)
        return countTags

    def getRelevantTags(self, countedTags):
        listofTuplesASC = sorted(countedTags.items(),  key=lambda x: x[1])
        # INVERTE A LISTA PARA PEGAR CONSIDERAR OS VALORES MAIS ALTOS PRIMEIRO (DECRESCENTE)
        listofTuplesDEC = listofTuplesASC[::-1]
        relevant_tags = []
        for elem in listofTuplesDEC:
            if(len(relevant_tags) <= 5):
                print(elem[0], " ::", elem[1])
                relevant_tags.append(elem[0])
            else:
                break
        print("relevant_tags => ", relevant_tags)
        return relevant_tags
