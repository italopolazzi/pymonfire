#Define aplication credentials
# Imports the Google Cloud client library
import six
import nltk
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from textblob import TextBlob
from textblob.exceptions import NotTranslated


class MyCloudProcessor:
	def __init__(self):
		self.client = language.LanguageServiceClient.from_service_account_json('tcclukeit-6018bd3fabd0.json')
		
	def sentiment(self, text = ''):
		document = types.Document( content=text, type=enums.Document.Type.PLAIN_TEXT)
		sentiment = self.client.analyze_sentiment(document=document).document_sentiment

		print('Text: {}'.format(text))
		print('Sentiment Score: {}, Magnitude: {}'.format(sentiment.score, sentiment.magnitude))
		return sentiment.score
	
	def transalate(self, text='', language='en'):
		result = TextBlob(text)
		if result.detect_language() != language:
			try:
				result = TextBlob(str(result.translate(to=language)))
			except NotTranslated:
				print('ERRO: Texto não pode ser traduzido! Tentativa     Texto:    ', text)
				return text
		
		return str(result)
		
	def classify(self, text=''):
		#text = text.lower()
		print(text)
		print('-------')
		if isinstance(text, six.binary_type):
			text = text.decode('utf-8')
		
		# Instantiates a plain text document.
		document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
		entities = self.client.analyze_entities(document).entities
		
		# entity types from enums.Entity.Type
		# entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
		#               'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
		
		result = {}
		for entity in entities:
			result.update({entity.name: entity.salience})
		result = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
		print(result)
		return result
	
'''
tx = 'Essa coca é Fanta. Ahh! me dáa Coca sempre foi o melhr refrigerante. E daí?'
mcp = MyCloudProcessor()
mcp.sentiment(tx)
mcp.classify(tx)'''


