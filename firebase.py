import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def firebase(firebase_collection):
  cred = credentials.Certificate('src/json/keys.json')
  firebase_admin.initialize_app(cred)

  db = firestore.client()

  users_ref = db.collection(firebase_collection)
  docs = users_ref.get()

  return docs