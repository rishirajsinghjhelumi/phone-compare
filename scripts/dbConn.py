from pymongo import MongoClient

def getMongoDBConn():
	
	client = MongoClient('localhost', 27017)
	return client['compareDB']