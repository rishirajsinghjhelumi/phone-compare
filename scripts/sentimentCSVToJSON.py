import json
from dbConn import getMongoDBConn

SENTIMENT_FILES = [
	"ParametricAnalysis/Count/Amazon.csv",
	"ParametricAnalysis/Count/Flipkart.csv",
	"ParametricAnalysis/Count/Snapdeal.csv"
]
sentimentJSON = {}

def getSentimentJSON(sentiment):

	fields = sentiment.split(',')
	for i in range(len(fields)):
		fields[i] = fields[i].strip()

	brand = fields[0]
	model = fields[1]
	about = fields[2]
	neg = fields[3]
	neu = fields[4]
	pos = fields[5]

	tup = (brand, model)
	if tup not in sentimentJSON:
		sentimentJSON[tup] = {
			"Brand" : brand,
			"Model Name" : model,
			"Sentiments" : []
		}

	sentimentJSON[tup]["Sentiments"].append({
		"About" : about,
		"Positive" : pos,
		"Negative" : neg,
		"Neutral" : neu
	})


def generateSentiments(filename):
	
	sentiments = open(filename).read().split('\n')[:-1]
	faults = 0

	for sentiment in sentiments:
		try:
			getSentimentJSON(sentiment)
		except:
			print "Fault in :", sentiment, filename
			faults += 1

	print faults

def storeInDB():

	mongo = getMongoDBConn()
	sentiments = mongo.sentiments
	for key in sentimentJSON:
		sentiments.insert(sentimentJSON[key])

if __name__ == '__main__':

	for fil in SENTIMENT_FILES:
		generateSentiments(fil)
	storeInDB()