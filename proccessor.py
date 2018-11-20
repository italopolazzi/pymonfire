from googlecloud import MyCloudProcessor as mgcp

class Proccessor:
    def __init__(self):
        self.tagger = mgcp()

    def proccess_one(self, text):
        sentimento = self.tagger.sentiment(text)#['sentimento']
        tags = self.tagger.classify(text)
        
        #print(u'Classify: {}  Tags: {}'.format(sentimento, tags))
        return {
            "classify": sentimento,
            "autoTag": tags
        }

    def proccess_many(self, array):
        temp = []
        for text in array:
            temp.append({
                "classify": self.tagger.sentiment(text)['sentimento'],
                "autoTag": self.tagger.classify(text)
            })
