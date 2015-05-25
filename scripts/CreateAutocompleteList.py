from os import listdir
from os.path import isfile, join
import json

from dbConn import getMongoDBConn
mongo = getMongoDBConn()
phonesDB = mongo.phones.find()
autoCompletePhones = mongo.autoCompletePhones
for phones in phonesDB:
	autoCompletePhones.insert({
		"Name" : phones["Brand"] + " " + phones["Model Name"] ,
		"_id" : phones["_id"]
	}) 

for phones in phonesDB:
	autoCompletePhones.insert({
		"Name" : phones["Brand"] 
	}) 