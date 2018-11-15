from tagger import Tagger as Tg

class Proccessor:
    def __init__(self):
        self.tagger = Tg()

    def proccess_one(self, text):
        return {
            "classify": self.tagger.classify(text)['sentimento'],
            "autoTag": self.tagger.autoTag(text)
        }

    def proccess_many(self, array):
        temp = []
        for text in array:
            temp.append({
                "classify": self.tagger.classify(text)['sentimento'],
                "autoTag": self.tagger.autoTag(text)
            })
