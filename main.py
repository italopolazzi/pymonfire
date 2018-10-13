from firebase import MyFirebase
from mongodb import MyMongo

class Pymonfire:
    collection = None
    collect = None

    def __init__(self, config):
        # Coleção de dados de onde serão trabalhados os documentos
        self.collection = config.get('collection', 'users')
        print(self.collection)
        # Variável de controle para coleatar dados do firebase
        # Ou armazenar no MongoDB
        # True: ativa as funções de trabalho com o Firebase
        # False: ativa as funções de trabalho com o MongoDB
        self.collect = config.get('collect', True)

    # Retorna o cursor com todos os documentos da coleção escolhida baseada na collect
    def queryCursors(self,):
        collection = self.collection
        return MyFirebase(collection).getDocs() if self.collect else MyMongo(collection).getDocs()

    # Percorre o cursor e imprime os dados
    def print(self):
        for doc in self.queryCursors():
            print(doc.to_dict() if self.collect else doc)


pmf = Pymonfire({'collect': False})
pmf.print()

