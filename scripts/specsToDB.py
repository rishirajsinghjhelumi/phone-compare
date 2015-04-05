from os import listdir
from os.path import isfile, join
import json

from dbConn import getMongoDBConn
mongo = getMongoDBConn()

SPECIFICATIONS_FOLDER = "PhoneSpecifications"

def store(filename):

	brand, model = None, None

	specs = json.loads(open(filename).read())["specification"]
	for spec in specs:
		if "GENERAL FEATURES" in spec:
			brand = spec["GENERAL FEATURES"]["Brand"]
			if "Model Name" in spec["GENERAL FEATURES"]:
				model = spec["GENERAL FEATURES"]["Model Name"]
			else:
				model = spec["GENERAL FEATURES"]["Model ID"]
			break

	
	specification = mongo.specification
	specification.insert({
		"Brand" : brand,
		"Model Name" : model,
		"specification" : specs
	})


def storeInDB():
	
	files = [ f for f in listdir(SPECIFICATIONS_FOLDER) if isfile(join(SPECIFICATIONS_FOLDER, f)) ]
	faults = 0

	for fil in files:
		try:
			store(SPECIFICATIONS_FOLDER + "/" + fil)
		except:
			faults += 1

	print faults

if __name__ == '__main__':

	storeInDB()
	