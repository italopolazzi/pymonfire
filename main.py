from firebase import firebase
from mongodb import mongodb

collection = 'users'

# true: {true => firebase, false => mongodb}, false: {false => firebase, true => mongodb}
coletar = not True

func = firebase(collection) if coletar else mongodb()

queryCursor = func

for doc in queryCursor:
    print(doc)
