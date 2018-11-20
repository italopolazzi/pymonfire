#Define aplication credentials
# Imports the Google Cloud client library
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from textblob import TextBlob
from textblob.exceptions import NotTranslated

#=============
# MyCloudProcessor tem o objetivo de fazer:
#  * Fazer análise de sentimento de um texto recebido como parâmetro
#  * Fazer seleção de tags para serem tidas como assuntos mais relevantes dentro do texto
#  * Tradução de textos caso necessário para melhor processamento
#=============
class MyCloudProcessor:
	def __init__(self): # Faz a inicialização do cliente
		self.client = language.LanguageServiceClient.from_service_account_json('tcclukeit-6018bd3fabd0.json')
		
	# Faz a analise de sentimentos do do text
	def sentiment(self, text=''):
		document = types.Document( content=text, type=enums.Document.Type.PLAIN_TEXT)
		sentiment = self.client.analyze_sentiment(document=document).document_sentiment

		#print('Text: {}'.format(text))
		# O atributo Score informa o valor do sentimento
		# O atributo magnitude é a 'força' daquele sentimento no texto. Como se fosse a potência.
		#print('Sentiment Score: {}, Magnitude: {}'.format(sentiment.score, sentiment.magnitude))
		
		# Retorna uma valor de -1 até 1 de acordo com a polaridade do sentimento
		# Onde:
		#   *  -1 é o máximo de sentimento negativo
		#   *   0 é o representa a neutralidade de sentimento
		#   *   1 é o sentimento mais positivo que o texto trás
		return sentiment.score
	
	# Faz a tradução do texto para a lin guageme scolhida de acordo com o suporte de idiomas do textblob
	def transalate(self, text='', language='en'):
		result = TextBlob(text)
		if result.detect_language() != language:
			try:
				result = TextBlob(str(result.translate(to=language)))
			except NotTranslated:
				print('ERRO: Texto não pode ser traduzido! Tentativa     Texto:    ', text)
				return text
		
		return str(result)
	
	# Classifica o texto recebido de acordo com as entidades identificadas e as retorna como tags de assunto.
	def classify(self, text=''):
		#print(text, '==============================================================')
		# para facilitar a analise, o texto é convertido para letras minúsculas
		text = text.lower()
		if isinstance(text, six.binary_type):
			text = text.decode('utf-8')
		
		# Instancia o texto como um documento plano
		document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
		# Chamada da função pelo cliente que irá retornar as entidades encontradas
		entities = self.client.analyze_entities(document).entities
		
		# entity types from enums.Entity.Type
		# entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
		#               'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
		
		result = {}
		#Selencionando os dados relevantes dentre as informações retornadas
		for entity in entities:
			result.update({entity.name: entity.salience})
		result = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
		#print(result)
		# retorna um array de strings com os nomes das entidades encontradas
		return result
	

# função para teste da classe
def test():
	tx = 'Essa coca é Fanta. Ahh! me dáa Coca sempre foi o melhr refrigerante. E daí?'
	mcp = MyCloudProcessor()
	mcp.sentiment(tx)
	mcp.classify(tx)

#test()


