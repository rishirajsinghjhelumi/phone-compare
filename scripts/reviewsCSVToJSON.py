import json

REVIEW_FILE = "Amazon.csv"
reviewJSON = {}

def getAbout(about):
	num, review = 0, None
	if about != '' and about != None and about != ' ':
		num = int(about.split(' ')[-1].split('(')[1].split(')')[0])
		review = ' '.join(about.split(' ')[:-1])

	return num, review

def getReviewJSON(review):

	fields = review.split(',')
	for i in range(len(fields)):
		fields[i] = fields[i].strip()

	brand = fields[0]
	model = fields[1]
	about = fields[2]
	numPos, reviewPos = getAbout(fields[3])
	numNeg, reviewNeg = getAbout(fields[4])

	tup = (brand, model)
	if tup not in reviewJSON:
		reviewJSON[tup] = {
			"Brand" : brand,
			"Model Name" : model,
			"Reviews" : []
		}

	found = 0
	for i in range(len(reviewJSON[tup]["Reviews"])):
		if reviewJSON[tup]["Reviews"][i]["About"] == about:
			found = 1

			if reviewPos != None:
				reviewJSON[tup]["Reviews"][i]["Positive"].append({
					"Review" : reviewPos,
					"Users" : numPos
				})

			if reviewNeg != None:
				reviewJSON[tup]["Reviews"][i]["Negative"].append({
					"Review" : reviewNeg,
					"Users" : numNeg
				})

	if found == 0:
		reviewJSON[tup]["Reviews"].append({
			"About" : about,
			"Positive" : [] if reviewPos == None else [{
					"Review" : reviewPos,
					"Users" : numPos
			}],
			"Negative" : [] if reviewNeg == None else [{
					"Review" : reviewNeg,
					"Users" : numNeg
			}],
		})

def generateReviews(filename):
	
	reviews = open(filename).read().split('\n')[:-1]
	faults = 0

	for review in reviews:
		try:
			getReviewJSON(review)
		except:
			print "Fault in :", review
			faults += 1

	print faults

if __name__ == '__main__':
	generateReviews(REVIEW_FILE)
	print json.dumps(reviewJSON[("Apple", "Apple iPhone 4")])
