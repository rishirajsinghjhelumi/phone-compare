from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from bson.objectid import ObjectId

from bson import json_util
import json

from app import mongo
from app import app
from app.decorators import mongoJsonify, jsonResponse
import logging
from app.util import getArgAsList
from logging.handlers import RotatingFileHandler

mod = Blueprint('phones', __name__, url_prefix='/phone')

formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler("./logs/application.log", maxBytes=10000000, backupCount=5)
#handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

def getPhoneInfo(phoneID):
	app.logger.info(phoneID)
	phone = mongo.phones.find_one({
		"_id" : ObjectId(phoneID)
	})
	
	try:
		phone["Reviews"] = mongo.reviews.find_one({
			"Brand" : phone["Brand"],
			"Model Name" : phone["Brand"] + " " + phone["Model Name"]
		})["Reviews"]
	except:
		 app.logger.error("Review data not found for phone with ID: ")
	try:
		prices = mongo.prices.find({
                        "Model Name" : phone["Brand"] + " " + phone["Model Name"]
                })
		eComList = []
		app.logger.info(prices)
		for price in prices:
			eCom = {}
			eCom["website"] = price["ECommerceName"]
			eCom["price"] = price["ECommercePrice"]
			eCom["stock status"] = price["ECommerceStatus"]
			eCom["productUrl"] = price["ECommercePdURL"]
			eComList.extend([eCom])
		phone["Prices"] = eComList
		app.logger.info("Prices Data====>")
		app.logger.info(phone["Prices"])
        except:
                app.logger.error("Price data not found for phone with ID: ")
                app.logger.error(phoneID)

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
		app.logger.info("Keywords Data ======>")
		app.logger.info(phone["Keywords"])
		
	except:
		app.logger.error("Sentiment data not found for phone with ID: ")
                app.logger.error(phoneID)

	return phone

def getPhoneIdListFromPriceRange(priceRange, brand):
	low = float(priceRange[0])
	app.logger.error(low)
	high = float(priceRange[1])
	phones = mongo.prices.find({ 'ECommercePrice' : {'$gte':low, '$lt':high}})
	phoneList = []
	phoneList = [phone["Model Name"].replace(phone["Brand"] + " ", "") for phone in phones]
        if brand:
	        phoneDetailList = [mongo.phones.find({"Model Name" : phoneName, "Brand":{"$in": brand}}) for phoneName in phoneList]
        else:
            phoneDetailList = [mongo.phones.find({"Model Name" : phoneName}) for phoneName in phoneList]
	phoneIdList = []
        for phoneDetail in phoneDetailList:
		for resultObj in phoneDetail:
			phoneIdList.append(resultObj['_id'])
			app.logger.info(resultObj['_id'])
	return  phoneIdList

def getPhoneIdListFromKeywordPreference(keyword):
	phones = mongo.keywords.find({"Keyword":keyword, "Rating": {'$gte': 3.5}})
	phoneList = []
        phoneList = [[phone["Brand"],phone["Model Name"].replace(phone["Brand"] + " ", "")] for phone in phones]
        phoneDetailList = [mongo.phones.find({"Model Name" : phoneName[1], "Brand":phoneName[0]}) for phoneName in phoneList]
        phoneIdList = []
        for phoneDetail in phoneDetailList:
                for resultObj in phoneDetail:
                        phoneIdList.append(resultObj['_id'])
                        app.logger.info(resultObj['_id'])
	app.logger.info("PhoneIds for keyword {}" , keyword)
        return  phoneIdList

@mod.route('/brand/<brandName>', methods=['GET'])
@jsonResponse
def brandModels(brandName):

	phones = mongo.phones.find({
		"Brand" : brandName
		}, {
		"Model Name" : 1
	})
	return [phone for phone in phones]

@mod.route('/detail/<phoneID>', methods=['GET'])
@jsonResponse
def phoneDetail(phoneID):

	return getPhoneInfo(phoneID)

@mod.route('/details', methods=['GET'])
@jsonResponse
def phones():
	phoneIds = getArgAsList(request, 'ids')
	priceRange = getArgAsList(request, 'pricerange')
	keywords = getArgAsList(request, 'keywords')
	brands = getArgAsList(request, 'brands')
	if phoneIds:
		return [getPhoneInfo(phone) for phone in phoneIds]
	elif priceRange or keywords:
		app.logger.info("Price range with keywords")
		phoneIds = []
		for keyword in keywords:
			phoneIds.extend(getPhoneIdListFromKeywordPreference(keyword))
		phoneIds = list(set(phoneIds))
		app.logger.info(phoneIds)
		priceFilterPhoneId = getPhoneIdListFromPriceRange(priceRange, brands)
		if keywords:
			phoneIds = set(phoneIds) & set(priceFilterPhoneId)
		elif priceRange:
			app.logger.info("only PriceRange")
			phoneIds = priceFilterPhoneId
		return [getPhoneInfo(phone) for phone in phoneIds]
        else :
                return keywords

def defineIndex():
    #mongo.phones.create_index( [{ 'Brand': 'text'}] )

#     mongo.Keywords.create_index([
#       ('Brand', 'text')
#   ],
#   name="search_index",
#   weights={
#       'Keyword':100
#   }
# )
    mongo.phones.drop_indexes()
    mongo.phones.create_index([
     ('Brand', 'text'),
     ('Model Name', 'text'),
     ('specification.GENERAL FEATURES.SIM Type', 'text'),
     ('specification.GENERAL FEATURES.Handset Color', 'text')
  ],
        cache_for=300,

  name="search_index",
  weights={
      'Brand':100,
      'Model Name':100,
      'specification.GENERAL FEATURES.SIM Type':100,
      'specification.GENERAL FEATURES.Handset Color':100
  }
)

def searchQuery(queryText):
    defineIndex()
    queryList = queryText.  split(" ")
    app.logger.info(queryList)
    idList = []
    for queryText in queryList:
        text_results = mongo.command('text', 'phones', search=queryText, limit=100)
        idList.extend([phone["obj"]["_id"] for phone in text_results["results"]])
    #idList = [ids[$oid] for ids in idList]
    idList = list(set(idList))
    return idList



		
