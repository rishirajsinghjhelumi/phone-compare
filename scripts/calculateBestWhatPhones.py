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

def getUnSortedPhoneListForKeywordWithFinalRating(keyword, phoneList):
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
							Pricefact = 1.05
						elif phoneLowest < 30000  and phoneLowest >= 20000:
							Pricefact = 1.1
						elif phoneLowest < 40000  and phoneLowest >= 30000:
							Pricefact = 1.15
						elif phoneLowest < 50000  and phoneLowest >= 40000:
							Pricefact = 1.2
						elif phoneLowest < 60000  and phoneLowest >= 50000:
							Pricefact = 1.2
						else:
							Pricefact = 1.2
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
		
		finalRating =  allPhones['Rating']*(1+1.7*(allPhones['Negative'] + allPhones['Positive'])/maxPosPlusNeg)*allPhones["Pricefact"]*10
		finalRating = round(finalRating,2)
		if finalRating >=  100.00:
			finalRating = 99.99
		allPhones['finalRating'] = finalRating
		if maxfinalRat < finalRating:
			maxfinalRat = finalRating
			maxfinalRatName = allPhones['ECommercePrice']
		finalPhoneList.append(allPhones)
	return finalPhoneList


def computeListAndPutToDB(finalPhoneList, keyword):
	finalPhoneList = sorted(finalPhoneList, key=lambda k: k['finalRating']) 
	finalPhoneList = finalPhoneList[::-1]
	print finalPhoneList
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
			tempPhoneDetail['finalRating'] = round(allPhones['finalRating'],2)
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

argList = []
argList =  sys.argv
argList.pop(0)
keyword = argList.pop(0)
#For All Best Reco
if keyword == "All":
	bestCollection = mongo.bestCollection
	bestKeyword = {'Camera':.25, 'Battery':.3, 'Low heating': .1,'Design and build quality': .2, 'Screen': .15}
	allPhones = []
	for phone in mongo.phones.find():
		allPhone = {}
		try:
			allPhone["_id"] = phone["_id"]
			allPhone["Model Name"] = phone["Brand"] + " " + phone["Model Name"]
			allPhone["Brand"] = phone["Brand"]
			allPhones.append(allPhone)
		except:
			pass
	allPhoneWithKeyWordRating = []
	allPhoneWithAllKeyWordRating = []
	keyPhoneDictWithFinalRating = []
	for keyword in bestKeyword:
		KeyWordSpecificList = []
		for phone in allPhones:
			keywordForPhone = mongo.keywords.find_one({'Model Name': phone['Model Name'], 'Keyword':keyword})
			if keywordForPhone == None:
				keywordForPhone = {'Rating': 0, 'Keyword': 'Battery', 'Positive': 0, 'Brand': phone["Brand"], 'Negative': 0, 'Neutral': 0, 'Model Name': phone['Model Name'], 'finaRating':0.0}
			KeyWordSpecificList.append(keywordForPhone)
		allPhoneWithKeyWordList =  getUnSortedPhoneListForKeywordWithFinalRating(keyword,KeyWordSpecificList)
		for iter in range(len(allPhoneWithKeyWordList)):
			try:
				localList = keyPhoneDictWithFinalRating[iter]
			except:
				localList = ['',0.0]
				keyPhoneDictWithFinalRating.append(localList)

			modelName = allPhoneWithKeyWordList[iter]['Model Name']
			finaRating = allPhoneWithKeyWordList[iter]['finalRating']
			localList = [modelName,round(localList[1]+finaRating*bestKeyword[keyword],2)]
			keyPhoneDictWithFinalRating[iter] = localList
	finalPhoneList = []
	for phones in keyPhoneDictWithFinalRating:
		phoneDict = {}
		phoneDict['Model Name'] = phones[0]
		phoneDict['finalRating'] = phones[1]
		finalPhoneList.append(phoneDict)
	computeListAndPutToDB(finalPhoneList, 'All')

else:
	#For Keyword Specific
	phoneList = mongo.keywords.find({'Keyword':keyword})
	finalPhoneList = []
	finalPhoneList = getUnSortedPhoneListForKeywordWithFinalRating(keyword, phoneList)
	computeListAndPutToDB(finalPhoneList, keyword)
		# print allPhones['TotalRating'], "," ,allPhones['ECommercePrice'], "," ,allPhones['Model Name'], "," ,allPhones['Rating'],"," , allPhones['Pricefact'], "," ,allPhones['Negative'], "," ,allPhones['Positive'] ,"," , finalRating





