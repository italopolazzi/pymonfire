import random
import datetime
import os
import json

from firebase import MyFirebase
from samples.users.users import users
from proccessor import Proccessor

REACTIONS_SIZE = 6

REACTIONS = {
    'positive': [0, 3, 5],
    'neutral': [2],
    'negative': [1, 4]
}

TOTAL_ANONYM = "total_anonym"

dirname = os.path.dirname(__file__)
SAMPLES_USERS_PATH = os.path.join(dirname, 'samples\questions_and_answers')


class Injector:
    def __init__(self):
        self.myFirebase = MyFirebase('questions')
        self.procc = Proccessor()
        self.users = users

        self.all_reactions = self.getAllReactions()

        self.iterateEachSample_UserFile()

    def getAllReactions(self):
        result = []
        for category in REACTIONS:
            result += REACTIONS[category]
        return result

    def validSize(self):
        q_len = len(self.questions)
        a_len = len(self.answers)
        if q_len != a_len:
            raise BaseException(
                "The total of questions and answers must be equal")
        return q_len

    '''
    # PERCORRE CADA ARQUIVO DE AMOSTRAS, CARREGA AS PERGUNTAS E RESPOSTAS E VALIDA SE O TAMANHO É IGUAL
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
                print("Size of {} validated! Total: {}".format(
                    filename, self.size))

                print("Generating appropriate reactions...")
                self.reactions = self.getReactions(
                    self.proccessAnswersPolarities())

                print("Iterating in each question and answers...")
                self.iterateEachQuestionAndAnswer()

    '''
    # DE ACORDO COM A POLARIDADE DA RESPOSTA SELECIONA UMA REAÇÃO ALEATORIAMENTE
    # MAIS ADEQUADA AO SENTIMENTO IDENTIFICADO NA RESPOSTA
    # ---------------- (-0,34) ---------------------- (0,32) ---------------------
    # ---- NEGATIVO ---------------- NEUTRO -------------------- POSITIVO --------
    '''

    def selectReactionBasedInPolarity(self, polarity):
        if polarity < -0.34:
            return random.choice(REACTIONS['negative'])
        elif polarity < 0.32:
            return random.choice(REACTIONS['neutral'])
        else:
            return random.choice(REACTIONS['positive'])

    '''
    # CHAMA AS FUNÇÃO QUE SELECIONA UMA REAÇÃO ADEQUADA PARA A POLARIDADE
    # SE A POLARIDADE NÃO ESTÁ IDENTIFICADA ENTÃO SELECIONA UMA REAÇÃO
    # TOTALMENTE ALEATÓRIA
    '''

    def getReactions(self, polarities):
        reactions = []
        for polarity in polarities:
            if(polarity != None):
                reactions.append(self.selectReactionBasedInPolarity(polarity))
            else:
                reactions.append(random.choice(self.all_reactions))
        return reactions

    '''
    # RETORNA UMA LISTA DE POLARIDADES DO MESMO TAMANHO 
    # DA AMOSTRA DE PERGUNTAS E RESPOSTAS.
    '''

    def proccessAnswersPolarities(self):
        print("Proccessing answers polarities...")
        polarities = []
        for answer in self.answers:
            try:
                polarities.append(self.procc.proccess_one(
                    answer)['classify'].polarity)
            except Exception as e:
                print("Erro na resposta => {}: {}".format(answer, e))
                polarities.append(None)
        print(polarities)
        print("SIZE(polarities) => {}".format(len(polarities)))
        return polarities

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
            result = self.myFirebase.createOne(question)
            print("\n\n{}".format(question))
            print("RESULT => {}".format(result))
        print("\n\nDATA INJECTED!")

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
                'reaction': self.reactions[index]
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
