from os import listdir
from os.path import isfile, join
import json, sys
from bson.objectid import ObjectId

from dbConn import getMongoDBConn

mongo = getMongoDBConn()
def getPhoneInfo(phoneID):
	phone = mongo.phones.find_one({
		"_id" : ObjectId(phoneID)
	})
	
	try:
		phone["Reviews"] = mongo.reviews.find_one({
			"Brand" : phone["Brand"],
			"Model Name" : phone["Brand"] + " " + phone["Model Name"]
		})["Reviews"]
	except:
		pass
		 # app.logger.error("Review data not found for phone with ID: ")
	try:
		prices = mongo.prices.find({
                        "Model Name" : phone["Brand"] + " " + phone["Model Name"]
                })
		eComList = []
		# app.logger.info(prices)
		for price in prices:
			eCom = {}
			eCom["website"] = price["ECommerceName"]
			eCom["price"] = price["ECommercePrice"]
			eCom["stock status"] = price["ECommerceStatus"]
			eCom["productUrl"] = price["ECommercePdURL"]
			eComList.extend([eCom])
		phone["Prices"] = eComList
		
        except:
        	pass
                # app.logger.error("Price data not found for phone with ID: ")
                # app.logger.error(phoneID)

	try:
		keywords = mongo.keywords.find({
			"Brand" : phone["Brand"],
			"Model Name" : phone["Brand"] + " " + phone["Model Name"]
		})
		eComList = []
		for keyword in keywords:
			eCom = {}
			eCom["Keyword"] = keyword["Keyword"]
			eCom["Negative"] = keyword["Negative"]
			eCom["Positive"] = keyword["Positive"]
			eCom["Neutral"] = keyword["Neutral"]
			eCom["Rating"] = keyword["Rating"]
			eComList.extend([eCom])
		phone["Keywords"] = eComList
		
		
	except:
		pass
		# app.logger.error("Sentiment data not found for phone with ID: ")
  #               app.logger.error(phoneID)

	return phone


argList = []
argList =  sys.argv
argList.pop(0)
keyword = argList.pop(0)
phoneList = mongo.keywords.find({'Keyword':keyword})
allKeywordPhoneList = []
finalPhoneList = []
maxPosPlusNeg = 0
for allPhones in phoneList:
	allReqPhoneDetails = {}
	phoneLowest = 0
	phoneName = allPhones['Model Name']
	Pricefact = 0
	
	phonePrice = mongo.prices.find({'Model Name':phoneName})
	for prices in phonePrice:
		realP = prices['ECommercePrice']
		if realP > 0:
			if prices['ECommerceStatus'] == 1:
				if phoneLowest < realP:
					phoneLowest = realP
					if phoneLowest < 10000:
						Pricefact = 1
					elif phoneLowest < 20000  and phoneLowest >= 10000:
						Pricefact = 1.15
					elif phoneLowest < 30000  and phoneLowest >= 20000:
						Pricefact = 1.3
					elif phoneLowest < 40000  and phoneLowest >= 30000:
						Pricefact = 1.45
					elif phoneLowest < 50000  and phoneLowest >= 40000:
						Pricefact = 1.6
					elif phoneLowest < 60000  and phoneLowest >= 50000:
						Pricefact = 1.6
					else:
						Pricefact = 1.6
	allReqPhoneDetails['ECommercePrice'] = phoneLowest
	if phoneLowest >0:
		PosPlusNeg = allPhones['Negative'] + allPhones['Positive']

		if maxPosPlusNeg < PosPlusNeg:
			maxPosPlusNeg = PosPlusNeg
		allReqPhoneDetails['TotalRating'] = PosPlusNeg
		allReqPhoneDetails['ECommercePrice'] = phoneLowest
		allReqPhoneDetails['Model Name'] = phoneName
		allReqPhoneDetails['Rating'] = allPhones['Rating']
		allReqPhoneDetails['Pricefact'] = Pricefact
		allReqPhoneDetails['Negative'] = allPhones['Negative']
		allReqPhoneDetails['Positive'] = allPhones['Positive']
		allKeywordPhoneList.append(allReqPhoneDetails)
		
maxfinalRat = 0
maxfinalRatName = 0
for allPhones in allKeywordPhoneList:
	finalRating = 0
	
	finalRating = allPhones['finalRating'] = allPhones['Rating']*(1+(allPhones['Negative'] + allPhones['Positive'])/maxPosPlusNeg)*allPhones["Pricefact"]*10
	if finalRating > 100:
		finalRating = 100
	if maxfinalRat < finalRating:
		maxfinalRat = finalRating
		maxfinalRatName = allPhones['ECommercePrice']
	finalPhoneList.append(allPhones)
	# print allPhones['TotalRating'], "," ,allPhones['ECommercePrice'], "," ,allPhones['Model Name'], "," ,allPhones['Rating'],"," , allPhones['Pricefact'], "," ,allPhones['Negative'], "," ,allPhones['Positive'] ,"," , finalRating

finalPhoneList = sorted(finalPhoneList, key=lambda k: k['finalRating']) 
finalPhoneList = finalPhoneList[::-1]
finalPhoneListWithScore = []
tempFinalList = []
for allPhones in finalPhoneList:
	tempPhoneDetail = {}
	brandName = allPhones['Model Name']
	brandName = brandName.split(" ")
	brandName.pop(0)
	brandName = " ".join(brandName)
	modelID = ""
	try:
		modelID = mongo.phones.find_one({'Model Name': brandName})['_id']
		tempPhoneDetail = getPhoneInfo(modelID)
		tempPhoneDetail['finalRating'] = allPhones['finalRating']
		finalPhoneListWithScore.append(tempPhoneDetail)
		
	except:
		pass

		# print allPhones['Model Name']

shortList = finalPhoneListWithScore[:15]
longList = finalPhoneListWithScore
bestCollection = mongo.bestCollection

bestKeyWordPhones = mongo.bestCollection.find({'keyword':keyword})
for allPhones in bestKeyWordPhones:
	mongo.bestCollection.remove(allPhones['_id'])

bestCollection.insert({
		'keyword' : keyword,
		"short" : shortList,
		"long" : longList
	})

bestKeyWordPhones = mongo.bestCollection.find({'keyword':keyword})
for allPhones in bestKeyWordPhones:
	print allPhones['_id']


print "Best" , keyword , "Uploaded"




