from textblob import TextBlob
from textblob import classifiers


import nltk
import json
import pickle

import os
dirname = os.path.dirname(__file__)
class Tagger:
	def __init__(self):
		try:
			print('Carregando classificador...')
			self.classifier = self._loadClassifier(os.path.join(dirname, 'classifier.obj'))
			print('Classificador carregado!')
		
		except FileNotFoundError:
			print('ERRO 404: Classificador não encontrado')
			print('Treinando novo classificador...')
			self.classifier = self._sentiTrain()
			print('Testando acuracidade do classificador')
			self._testClassifier()
			print('Salvando novo classificador em "./classifier.obj"')
			self._saveClassifier(self.classifier,os.path.join(dirname, 'classifier.obj'))
		
		print ('Tagger iniciado!\n')

	def classify(self, text):
		
		result = TextBlob(text)
		if result.detect_language() != 'en':
			result = TextBlob(str(result.translate(to='en')))
		
		final = {'texto':text, 'english':str(result), 'sentimento':result.sentiment}
		print(final)
		return final
	
	def autoTag(self, text, number_tags = 5):
		print('Identificando palavras-chave...')
		#Conujunto de tags que serão filtradas como recomendação de assuntos
		type_selection = ("NNP", "NNPS")
		# NN   = Noun, singular or mass
		# NNS  = Noun, plural
		# NNP  = Proper noun, singular
		# NNPS = Proper noun, plural
		# Referência para estas tags: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
		
		tx = TextBlob(text)
		if tx.detect_language() != 'en':
			text = str(tx.translate(to='en'))
		
		tknized = nltk.pos_tag(nltk.word_tokenize(text))
		tags = []
		sinal =''
		for (word, word_type) in tknized:
			if word in ['@', '#']:
				sinal = word
				continue
			if sinal is not '':
				word = sinal+word
				sinal = ''
			print(word,word_type)
			for type in type_selection:
				if word_type in type:
					tags.append(word)
		tags = sorted(set(tags))
		print("Chaves encontradas: " , tags)
		return tags
	
	
	def _sentiTrain(self):
		print('Treinando classificador de sentimento...')
		training = self._loadTrainData(os.path.join(dirname, 'data_senti.json'))
		classifier = classifiers.NaiveBayesClassifier(training)
		classifier.show_informative_features(1)
		blob = TextBlob('', classifier=classifier)
		print (blob.classify())
		return classifier
	
	def _testClassifier(self):
		testing = [
			('Superman was never an interesting character.', 'pos'),
			('Fantastic Mr Fox is an awesome film!', 'neg'),
			('Dragonball Evolution is simply terrible!!', 'pos')
		]
		
		print('Teste de acuracidade:')
		print(self.classifier.accuracy(testing))
		
	def _loadTrainData(self, path):
		file = open(path, 'rb')
		data = json.load(file)
		file.close()
		return data
	
	def _loadClassifier(self, path):
		load_training = open(path, 'rb')
		new_cl = pickle.load(load_training)
		load_training.close()
		return new_cl
	
	def _saveClassifier(classifier, path):
		f = open(path, 'wb')
		pickle.dump(classifier,f)
		f.close()
