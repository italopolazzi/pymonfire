# -*- coding: utf-8 -*-
from firebase import MyFirebase
from mongodb import MyMongo
# from datetime import datetime, timezone
from sample import document_to_update

class Pymonfire:
    collection = None
    collect = None

    def __init__(self, config = {}):
        # Coleção de dados de onde serão trabalhados os documentos
        self.collection = config.get('collection', 'users')
        # Variável de controle para coleatar dados do firebase
        # Ou armazenar no MongoDB
        # True: ativa as funções de trabalho com o Firebase
        # False: ativa as funções de trabalho com o MongoDB
        self.collect = config.get('collect', True)

        # Classes de gerenciamento dos bancos
        self.myMongo = MyMongo(self.collection)
        self.myFirebase = MyFirebase(self.collection)



    # Retorna o cursor com todos os documentos da coleção escolhida baseada na collect
    def queryCursors(self):
        return self.myFirebase.getDocs() if self.collect else self.myMongo.getDocs()

    # Percorre o cursor e imprime os dados
    def print_it(self):
        for doc in self.queryCursors():
            print(doc.to_dict() if self.collect else doc)

    def mgInsertOne(self, datum):
        return self.myMongo.insertOne(datum)

    def mgGetWhere(self, params):
        return self.myMongo.getWhere(params)

    def mgSetCollection(self, collection):
        self.myMongo.setCollection(collection)

    def fbSetCollection(self, collection):
        self.myFirebase.setCollection(collection)

    def fbUpdateOne(self, data):
        id = data["_id"]
        return self.myFirebase.updateOne(id, data)

    def fbGetWhere(self, k, o, v):
        return self.myFirebase.getWhere(k, o, v)

    def fbGetWhereAnd(self, k1, o1, v1, k2, o2, v2):
        return self.myFirebase.getWhereAnd(k1, o1, v1, k2, o2, v2)
