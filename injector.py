import random
import datetime
import os
import json

from firebase import MyFirebase
from samples.users.users import users

REACTIONS_SIZE = 6
TOTAL_ANONYM = "total_anonym"

dirname = os.path.dirname(__file__)
SAMPLES_USERS_PATH = os.path.join(dirname, 'samples\questions_and_answers')

class Injector:
    def __init__(self):
        self.tccFirebase = MyFirebase('questions')
        self.iterateEachSample_UserFile()
        # self.answers = answers
        # self.questions = questions
        # self.size = self.validSize()
        # self.users = users
        # print(users)
        # self.iterateEachQuestionAndAnswer()

    def validSize(self):
        q_len = len(self.questions)
        a_len = len(self.answers)
        if q_len != a_len:
            raise BaseException(
                "Não é possível iterar sobre amostras de perguntas e respostas de tamanhos diferentes")
        return q_len

    def iterateEachSample_UserFile(self):
        for filename in os.listdir(SAMPLES_USERS_PATH):
            if(filename.startswith('sample_')):
                fulldir = "{}\\{}".format(SAMPLES_USERS_PATH, filename)
                print(fulldir)
                fjson = json.load(filename)
                print(fjson)

    def iterateEachQuestionAndAnswer(self):
        for i in range(self.size):
            sender, recipient = self.selectRandomSenderAndRecipient()
            question = self.mountQuestion(i, sender, recipient)
            result = self.tccFirebase.createOne(question)
            print("\n\n{}".format(question))
            print("RESULT => {}".format(result))
        print("\n\nDATA INJECTED!")

    # DEFINE O MODO ANÔNIMO ALEATORIAMENTE OU AUTOMÁTICO SE O SENDER
    # TIVER SIDO ALEATORIAMENTE SELECIONADO COMO O TOTAL_ANONYM
    def getAnonymMode(self, sender):
        if(sender == TOTAL_ANONYM):
            return True
        else:
            return random.choice([True, False])

    def selectRandomSenderAndRecipient(self):
        sender = random.choice(self.users)
        while True:
            recipient = random.choice(self.users)
            if (recipient['id'] != TOTAL_ANONYM and recipient != sender):
                break
        # print("sender, recipient = ", sender, recipient)
        return sender, recipient

    def mountQuestion(self, i, sender, recipient):
        if(recipient['isFake']):
            return self.mountQuestionWithAnswer(i, sender['id'], recipient['id'])
        else:
            return self.mountQuestionWithoutAnswer(i, sender['id'], recipient['id'])

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
