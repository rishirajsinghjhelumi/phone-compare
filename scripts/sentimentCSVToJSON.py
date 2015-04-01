import json

SENTIMENT_FILE = "Amazon_Sentiment.csv"
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
			print "Fault in :", sentiment
			faults += 1

	print faults

if __name__ == '__main__':
	generateSentiments(SENTIMENT_FILE)
	print json.dumps(sentimentJSON[("Apple", "Apple iPhone 4")])
