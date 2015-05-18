from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from bson.objectid import ObjectId

from bson import json_util
import json

from app import mongo
from app import app
from app.phones.views import *
from app.cart.views import *
from app.decorators import mongoJsonify, jsonResponse
import logging
from app.util import getArgAsList
from logging.handlers import RotatingFileHandler
import jinja2

mod = Blueprint('webpage', __name__, url_prefix='')

formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler("./logs/application.log", maxBytes=10000000, backupCount=5)
#handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

@mod.route('/hello2', methods=['GET'])
def hello2():
	return "hello2"

@mod.route('/pdp/<phoneID>', methods=['GET'])
def productDetail(phoneID):
	phoneDetails = getPhoneInfo(phoneID)
	phoneName = phoneDetails["Model Name"]
	phoneBrand = phoneDetails["Brand"]
	title = phoneBrand + " " + phoneName
	cartDetails = getCartDetails()

	app.logger.info(cartDetails)
	for ids in cartDetails:
		app.logger.info(ids)
	return render_template("product-elevatezoom.html", title=title, phoneDetails = phoneDetails, cartDetails = cartDetails)

@mod.route('/compare', methods=['GET'])
def compareProducts():
	phoneIds = []
	phoneIds = getArgAsList(request, 'ids')
	app.logger.info(phoneIds)
	if not phoneIds:
		phoneIds = getCartDetails()
		app.logger.info("getting phoneIds from cart")
		app.logger.info(len(phoneIds))
	phoneDetails = [getPhoneInfo(phoneId) for phoneId in phoneIds]
	sampleProductDetail = getPhoneInfo("553171f5b7e36a714fd0bed5")
	app.logger.info(phoneIds)
	for phones in phoneDetails:
		app.logger.info(phones["Brand"])
	return render_template("compare.html", title="Compare Your Options", phoneDetails = phoneDetails, cartDetails = phoneIds, sampleProductDetail = sampleProductDetail)

@mod.route('/search',methods=['GET'])
def searchResults():
	cartList = getCartDetails()
	phoneIds = getArgAsList(request, 'ids')
	priceRange = getArgAsList(request, 'pricerange')
	keywords = getArgAsList(request, 'keywords')
	brands = getArgAsList(request, 'brands')
        weights = getArgAsList(request, 'weights')
	phoneList = []
	if phoneIds:
		phoneList =  [getPhoneInfo(phone) for phone in phoneIds]
	elif priceRange or keywords:
		app.logger.info("Price range with keywords")
		phoneIds = []
		for keyword in keywords:
			phoneIds.extend(getPhoneIdListFromKeywordPreference(keyword))
		phoneIds = list(set(phoneIds))
		app.logger.info(phoneIds)
		priceFilterPhoneId = getPhoneIdListFromPriceRange(priceRange,brands)
		if keywords:
			phoneIds = set(phoneIds) & set(priceFilterPhoneId)
		elif priceRange:
			app.logger.info("only PriceRange")
			phoneIds = priceFilterPhoneId
		phoneList =  [getPhoneInfo(phone) for phone in phoneIds]

        sortedPhoneList = sortPhoneList(phoneList, keywords, weights)
        phoneList = [sorted[0] for sorted in sortedPhoneList]
        scoreList = [sorted[1] for sorted in sortedPhoneList]
	return render_template("listing_usual.html", title = "Your choice Your Device", phoneDetails = phoneList, cartDetails = cartList, scoreList = scoreList)

def sortPhoneList(phoneList, keywords, weights):
    app.logger.info("in sorting")
    app.logger.info(weights)
    sortedPhoneList = []
    phoneScoreList = []

    maxPopulation = 0
    if weights == []:
        for key in keywords:
            weights.extend([5])

    for phIter in range(len(phoneList)):
        keyCount = 0
        keySum = 0
        population = 0
        phoneKeyWords = phoneList[phIter]["Keywords"]
        if len(keywords) == 0:
            app.logger.info("without keywords")
            for keys in phoneKeyWords:
                    population = population + keys["Positive"] + keys["Neutral"] + keys["Negative"]
            if maxPopulation < population:
                        app.logger.info("calculating maxPopulation")
                        app.logger.info(phoneList[phIter]["Model Name"])
                        app.logger.info(population)
                        maxPopulation = population
        else:
            app.logger.info("keywords")
            for keyIter in range(len(keywords)):
                phoneKeyWords = phoneList[phIter]["Keywords"]
                for keys in phoneKeyWords:
                    if keys["Keyword"] == keywords[keyIter]:
                        population = population + keys["Positive"] + keys["Neutral"] + keys["Negative"]
                if maxPopulation < population:
                            maxPopulation = population


    for phIter in range(len(phoneList)):
        keyCount = 0
        keySum = 0.0
        population = 0
        phoneKeyWords = phoneList[phIter]["Keywords"]
        if len(keywords) == 0:
            app.logger.info("without keywords")
            for keys in phoneKeyWords:
                    population = population + keys["Positive"] + keys["Neutral"] + keys["Negative"]
                    try:
                        keySum = keySum + keys["Rating"]*weights[keyCount]/5
                    except:
                        keySum = keySum + keys["Rating"]

                    keyCount = keyCount + 1
        else:
            app.logger.info("keywords")
            for keyIter in range(len(keywords)):
                for keys in phoneKeyWords:
                    if keys["Keyword"] == keywords[keyIter]:
                        population = population + keys["Positive"] + keys["Neutral"] + keys["Negative"]
                        keySum = keySum + (keys["Rating"])*(float(weights[keyCount]))/5
                        keyCount = keyCount + 1
        try:
                keyAvgScrore = ((keySum/keyCount) + ((population*5)/maxPopulation))/2
        except:
            keyAvgScrore = -1
        app.logger.info(keyAvgScrore*20)
        if keyAvgScrore!= -1:
            phoneScoreList.append([phoneList[phIter] ,int(keyAvgScrore*20)])
            phoneScoreList = sorted(phoneScoreList,key=lambda l:l[1],reverse=True)

    return phoneScoreList

@mod.route('/query', methods=['GET'])
def search():
    cartList = getCartDetails()
    queryText = getArgAsList(request, 'queryText')
    queryText = queryText[0]
    text_results = searchQuery(queryText)
    phoneList =  [getPhoneInfo(phone) for phone in text_results]
    sortedPhoneList = sortPhoneList(phoneList, [], [])
    phoneList = [sorted[0] for sorted in sortedPhoneList]
    scoreList = [sorted[1] for sorted in sortedPhoneList]
    return render_template("listing_usual.html", title = "Search result for " + queryText, phoneDetails = phoneList, cartDetails = cartList, scoreList = scoreList)
    # return phoneList



