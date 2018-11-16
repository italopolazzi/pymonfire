import random
import datetime
import os
import json

from firebase import MyFirebase
from samples.users.users import users
from proccessor import Proccessor

REACTIONS_SIZE = 6
TOTAL_ANONYM = "total_anonym"

dirname = os.path.dirname(__file__)
SAMPLES_USERS_PATH = os.path.join(dirname, 'samples\questions_and_answers')

class Injector:
    def __init__(self):
        self.myFirebase = MyFirebase('questions')     
        self.procc = Proccessor()
        self.users = users
        self.iterateEachSample_UserFile()

    def validSize(self):
        q_len = len(self.questions)
        a_len = len(self.answers)
        if q_len != a_len:
            raise BaseException(
                "The total of questions and answers must be equal")
        return q_len

    '''
    # PERCORRE CADA ARQUIVO DE AMOSTRAS, CARREGA AS PERGUNTAS E RESPOSTAS E VÁLIDAS SE O TAMANHO É IGUAL
    '''
    def iterateEachSample_UserFile(self):
        for filename in os.listdir(SAMPLES_USERS_PATH):
            if(filename.startswith('sample_')):
                file_directory = "{}\\{}".format(SAMPLES_USERS_PATH, filename)
                
                print("Loading {}...".format(filename))
                json_data = open(file_directory).read()
                data = json.loads(json_data)
                self.questions = data['questions']
                self.answers = data['answers']
                self.size = self.validSize()
                print("Size of {} validated! Total: {}".format(filename, self.size))

                print("Proccessing answers classifies...")
                self.reactions = self.procc.proccess_many(self.answers)
                print(self.reactions)

                # self.iterateEachQuestionAndAnswer()

    '''
    # REALIZA A SEGUINTE SEQUÊNCIA: 
    # PERCORRE CADA PERGUNTA E RESPOSTA,
    # SELECIONANDO USUÁRIO REMETENTES E DESTINATÁRIOS ALEATÓRIOS
    # MONTA A PERGUNTA FAKE, E ENVIA PARA O FIREBASE
    # E SE TUDO DER CERTO PRINTA O RESULTADO
    '''
    def iterateEachQuestionAndAnswer(self):
        for i in range(self.size):
            sender, recipient = self.selectRandomSenderAndRecipient()
            question = self.mountQuestion(i, sender, recipient)
            # result = self.myFirebase.createOne(question)
            # print("\n\n{}".format(question))
            # print("RESULT => {}".format(result))
        # print("\n\nDATA INJECTED!")

    '''
    # DEFINE O MODO ANÔNIMO ALEATORIAMENTE OU AUTOMÁTICO SE O SENDER
    # TIVER SIDO ALEATORIAMENTE SELECIONADO COMO O TOTAL_ANONYM
    '''
    def getAnonymMode(self, sender):
        if(sender == TOTAL_ANONYM):
            return True
        else:
            return random.choice([True, False])

    '''
    # SELECIONA UM REMETENTE E DESTINATÁRIO ALEATÓRIO
    # O DESTINATÁRIO DEVE SE DIFERIR DO USUÁRIO TOTAL_ANONYM
    # E NÃO PODE SER O MESMO QUE O REMETENTE
    '''
    def selectRandomSenderAndRecipient(self):
        sender = random.choice(self.users)
        while True:
            recipient = random.choice(self.users)
            if (recipient['id'] != TOTAL_ANONYM and recipient != sender):
                break
        # print("sender, recipient = ", sender, recipient)
        return sender, recipient

    '''
    # SE O USUÁRIO DESTINATÁRIO É FAKE
    # ENTÃO JÁ JÁ A FUNÇÃO PARA CRIAR UMA PERGUNTA COM RESPOSTA PRONTA
    # SE NÃO CRIA UMA SEM RESPOSTA PARA QUE O NÃO-FAKE POSSA RESPONDER
    '''
    def mountQuestion(self, i, sender, recipient):
        if(recipient['isFake']):
            return self.mountQuestionWithAnswer(i, sender['id'], recipient['id'])
        else:
            return self.mountQuestionWithoutAnswer(i, sender['id'], recipient['id'])

    '''
    # CRIA UMA PERGUNTA COM RESPOSTA PARA O FAKE
    '''
    def mountQuestionWithAnswer(self, index, sender_id, recipient_id):
        return {
            'text': self.questions[index],
            'anonym': self.getAnonymMode(sender_id),
            'sender': sender_id,
            'recipient': recipient_id,
            'sendedAt': str(datetime.datetime.now()),
            'status': 1,
            'answer': {
                'text': self.answers[index],
                'reaction': random.choice(range(REACTIONS_SIZE))
            }
        }

    '''
    # CRIA UMA PERGUNTA SEM RESPOSTA PARA QUE O NÃO-FAKE POSSA RESPONDER
    '''
    def mountQuestionWithoutAnswer(self, index, sender_id, recipient_id):
        return {
            'text': self.questions[index],
            'anonym': self.getAnonymMode(sender_id),
            'sender': sender_id,
            'recipient': recipient_id,
            'sendedAt': str(datetime.datetime.now()),
            'status': 0,
            'answer': None
        }


if __name__ == "__main__":
    injector = Injector()
