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
import os.path

mod = Blueprint('webpage', __name__, url_prefix='')
allBrands = ['Apple','Blackberry','Xiaomi','OnePlus','A&K','Celkon','Gionee','HTC','Huawei','Karbonn','Lava','Lenovo','LG','Micromax','Motorola','Microsoft','Nokia','Panasonic','Samsung','Sony','Spice','XOLO','Adcom','Agtel','Akai','Acer','Alcatel','AirTyme','AIEK','Alpha','Ambrane','Anand','Andi','AOC','Apollo','Arise','AsiaFone','a-star','Asus','ATOM','Beetel','Best','Beven','Beyond','Binatone','Bingo','Bloom','Blu','BQ','Brillon','Bsnl','BY2','Byond','Camerii','Cfore','Cheers','Chilli','CLOUD','Coolwave','Croma','Cubit','Daimond','Datawind','Devante','iball','YU']
allKeywords = ['Applications', 'Battery', 'Camera', 'Delivery and service', 'Design and build quality','Earphone', 'Front Camera', 'Gaming', 'Internet and Browsing', 'Less lag', 'Low heating', 'Music', 'Others', 'Price worthiness', 'Screen', 'Sound', 'UI', 'Video']
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

	app.logger.info(phoneDetails)
	for ids in cartDetails:
		app.logger.info(ids)
	return render_template("product-elevatezoom.html", title=title, phoneDetails = phoneDetails, cartDetails = cartDetails,allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18])

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
	sampleProductDetail = getPhoneInfo("557e55600c677c1bd4b187d6")
	app.logger.info(phoneIds)
	for phones in phoneDetails:
		app.logger.info(phones["Brand"])
	return render_template("compare.html", title="Compare Your Options", phoneDetails = phoneDetails, cartDetails = phoneIds, sampleProductDetail = sampleProductDetail,allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18])

@mod.route('/search',methods=['GET'])
def searchResults():
	phoneIds = getArgAsList(request, 'ids')
	priceRange = getArgAsList(request, 'pricerange')
	keywords = getArgAsList(request, 'keywords')
	brands = getArgAsList(request, 'brands')
        emptyResultsFlag = 0
        
        sortedPhoneList = []
        page = getArgAsList(request, 'page')
        weights = getArgAsList(request, 'weights')
        if priceRange == []:
            priceRange = [0,80000]
        else:
            priceRange = [int(priceRange[0]), int(priceRange[1])]
        sortedPhoneList = []
	if phoneIds:
		phoneList =  [getPhoneInfo(phone) for phone in phoneIds]
        elif keywords == []:
            phoneList = mongo.bestCollection.find_one({'keyword':'All'})
            phoneList = phoneList['long']

            sortedPhoneList = applyBrandAndPriceFilters(phoneList,brands, keywords,priceRange)
            if sortedPhoneList == []:
                emptyResultsFlag = 1
                sortedPhoneList = applyBrandAndPriceFilters(phoneList,brands, keywords,[0,80000])
            sortedPhoneList = sortedPhoneList[:120]
        else:
            if weights == []:
                weights = [0 for key in keywords]
            divFactor = len(keywords)
            if divFactor == 0:
                divFactor = 1
            phoneDict = {}
            allKeyWordPhoneList = []
            for keyword in keywords:
                keyWordPhoneList = mongo.bestCollection.find_one({'keyword': keyword})
                keyWordPhoneList = keyWordPhoneList['long']
                # keyWordPhoneList = applyBrandAndPriceFilters(keyWordPhoneList,brands, keywords,priceRange)
                allKeyWordPhoneList.extend(keyWordPhoneList)
            for phones in allKeyWordPhoneList:
                localDict = {}
                try:
                    localDict = phoneDict[phones['Model Name']]
                    localRating = phones['finalRating']/divFactor
                    localDict['finalRating'] = localDict['finalRating']/divFactor + localRating
                except:
                    localDict = phones
                    localRating = phones['finalRating']/divFactor
                    localDict['finalRating'] = localRating
                
                
                localDict['finalRating'] = round(localDict['finalRating'],2)
                phoneDict[phones['Model Name']] = localDict
            for phone in phoneDict:
                sortedPhoneList.append(phoneDict[phone])
            sortedPhoneList = applyBrandAndPriceFilters(sortedPhoneList,brands, keywords,priceRange)
            if sortedPhoneList == []:
                emptyResultsFlag = 1
                sortedPhoneList = applyBrandAndPriceFilters(sortedPhoneList,brands, keywords,[0,80000])
            sortedPhoneList = sorted(sortedPhoneList,key=lambda l:l[1],reverse=True) 

            sortedPhoneList = sortedPhoneList[:120]
                
        return displaySearchResults("search",sortedPhoneList, page,priceRange,keywords,brands,allKeywords,allBrands, emptyResultsFlag)
        # return render_template("listing_usual.html", title = "Your choice Your Device", phoneDetails = phoneList, cartDetails = cartList, scoreList = scoreList)

def applyBrandAndPriceFilters(phoneList, brands, keywords, priceRange):
    print brands
    print priceRange
    sortedPhoneList = []
    app.logger.info(brands)
    for allPhones in phoneList:
        brandFlag = 0
        priceFlag = 0
        phBrand = allPhones['Brand']
        phPrice = allPhones['Prices']
        if brands == []:
            brandFlag = 1
        elif phBrand in brands:
            brandFlag = 1
        else:
            brandFlag = 0

        if priceRange == [0,70000]:
            priceFlag = 1
        else:
            lowestPrice = 100000
            for prices in phPrice:
                if lowestPrice > prices['price'] and prices['price'] != 0:
                    lowestPrice = prices['price']
            if lowestPrice == 0 :
                app.logger.info("lowestPrice is zero")
                priceFlag = 0
            elif lowestPrice > priceRange[0] and lowestPrice <= priceRange[1]:
                priceFlag = 1                
        if brandFlag and priceFlag:
            sortedPhoneList.append([allPhones, allPhones['finalRating']])
    return sortedPhoneList
def get_unique_items(list_of_dicts):
    # Count how many times each key occurs.
    key_count = collections.defaultdict(lambda: 0)
    for d in list_of_dicts:
        key_count[d[key]] += 1

    # Now return a list of only those dicts with a unique key.
    return [d for d in list_of_dicts if key_count[d[key]] == 1]

def getListWhoseImageExist(phoneList):
    for phones in phoneList:
        modelName = phones["Brand"] + " " + phones["Model Name"]
        imagePath = "/static/img/ImageScrappers/" + modelName.strip() + ".jpg"
        print imagePath
        if os.path.isfile(imagePath):
            print modelName
    return phoneList
def displaySearchResults(pageType, sortedPhoneList, pageNo, priceRange,keywords,brands,allKeywords,allBrands, emptyResultsFlag):
    currentURL = request.url
    if pageNo:
        currentURL = currentURL[:-1]
    else:
        currentURL = currentURL + "&page="
    cartList = getCartDetails()
    items = len(sortedPhoneList)
    if items % 15 == 0:
        totalPages = items/15
    else:
        totalPages = items/15 + 1
    phoneList = [sort[0] for sort in sortedPhoneList]
    scoreList = [sort[1] for sort in sortedPhoneList]
    
    if not pageNo:
        if items > 15:
            return render_template("listing_usual.html", title = "Your choice Your Device", phoneDetails = phoneList[0:15], cartDetails = cartList, scoreList = scoreList[0:15], prev = 0, next = 2, totItem = items, page = 1, fromItem = 1, toItem = 15, currentURL = currentURL,totalPages = totalPages,allBrands = allBrands, allKeywords = allKeywords, priceRange = priceRange, selectedBrands = brands,selectedKeywords = keywords, pageType=pageType,allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18], emptyResultsFlag = emptyResultsFlag)
        else :
            return render_template("listing_usual.html", title = "Your choice Your Device", phoneDetails = phoneList, cartDetails = cartList, scoreList = scoreList, prev = 0, next = 0, totItem = items, page=0, fromItem = 1, toItem = items, currentURL = currentURL, totalPages = totalPages,allBrands = allBrands, allKeywords = allKeywords, priceRange = priceRange, selectedBrands = brands,selectedKeywords = keywords,pageType=pageType,allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18], emptyResultsFlag = emptyResultsFlag)
    else:
        pageNo = int(pageNo[0])
        if items > 15*pageNo:
            return render_template("listing_usual.html", title = "Your choice Your Device", phoneDetails = phoneList[15*(pageNo-1):(15*(pageNo))], cartDetails = cartList, scoreList = scoreList[15*(pageNo-1):15*(pageNo)], prev = 1, next = pageNo + 1, totItem = items, page = pageNo, fromItem = 15*(pageNo-1) + 1, toItem = 15*pageNo, currentURL = currentURL, totalPages = totalPages,allBrands = allBrands, allKeywords = allKeywords, priceRange = priceRange, selectedBrands = brands,selectedKeywords = keywords, pageType=pageType, emptyResultsFlag = emptyResultsFlag)
        else:
            return render_template("listing_usual.html", title = "Your choice Your Device", phoneDetails = phoneList[(15*(pageNo-1)):items], cartDetails = cartList, scoreList = scoreList[(15*pageNo-1):items], prev = 1, next = 0, totItem = items, page = pageNo, fromItem = 15*(pageNo-1) + 1, toItem = items, currentURL = currentURL, totalPages = totalPages,allBrands = allBrands, allKeywords = allKeywords, priceRange = priceRange, selectedBrands = brands,selectedKeywords = keywords,pageType=pageType, emptyResultsFlag = emptyResultsFlag)
    return render_template("listing_usual.html", title = "Your choice Your Device", phoneDetails = phoneList, cartDetails = cartList,priceRange = priceRange, scoreList = scoreList,allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18], emptyResultsFlag = emptyResultsFlag)

def addBazaarFundaScore(phoneList, keywords, weights):
    app.logger.info("in sorting")
    sortedPhoneList = []
    phoneScoreList = []
    app.logger.info(len(phoneList))
    maxPopulation = 1
    if weights == []:
        for key in keywords:
            weights.extend([5])

    for phIter in range(len(phoneList)):
        keyCount = 0
        keySum = 0
        population = 0
        phoneKeyWords = phoneList[phIter]["Keywords"]
        if len(keywords) == 0:
            for keys in phoneKeyWords:
                    population = population + keys["Positive"] + keys["Neutral"] + keys["Negative"]
            if maxPopulation < population:
                        maxPopulation = population
        else:
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
            for keys in phoneKeyWords:
                    population = population + keys["Positive"] + keys["Neutral"] + keys["Negative"]
                    try:
                        keySum = keySum + keys["Rating"]*weights[keyCount]/5
                    except:
                        keySum = keySum + keys["Rating"]

                    keyCount = keyCount + 1
        else:
            for keyIter in range(len(keywords)):
                for keys in phoneKeyWords:
                    if keys["Keyword"] == keywords[keyIter]:
                        population = population + keys["Positive"] + keys["Neutral"] + keys["Negative"]
                        keySum = keySum + (keys["Rating"])*(float(weights[keyCount]))/5
                        keyCount = keyCount + 1
        try:
                keyAvgScrore = ((keySum/keyCount) + ((population*5)/maxPopulation))/2
        except:
            keyAvgScrore = (population*5)/(maxPopulation)
            # keyAvgScrore = -1
        if keyAvgScrore!= -1:
            phoneScoreList.append([phoneList[phIter] ,int(keyAvgScrore*20)])
            #phoneScoreList = sorted(phoneScoreList,key=lambda l:l[1],reverse=True)
    # app.logger.info(len(phoneScoreList))
    return phoneScoreList

@mod.route('/search/query', methods=['GET'])
def search():

    
    queryText = getArgAsList(request, 'queryText')
    queryText = queryText[0]
    
    text_results = searchQuery(queryText)
    phoneList =  [getPhoneInfo(phone) for phone in text_results]
    sortedPhoneList = addBazaarFundaScore(phoneList, [], [])
    page = getArgAsList(request, 'page')
    app.logger.info(page)
    
    return displayQueryResults("query", sortedPhoneList, page, [])

def displayQueryResults(pageType, sortedPhoneList, pageNo, priceRange):
    currentURL = request.url
    if pageNo:
        currentURL = currentURL[:-1]
    else:
        currentURL = currentURL + "&page="
    app.logger.info(currentURL)
    app.logger.info(pageNo)
    cartList = getCartDetails()
    items = len(sortedPhoneList)
    if items % 20 == 0:
        totalPages = items/20
    else:
        totalPages = items/20 + 1
    phoneList = [sort[0] for sort in sortedPhoneList]
    scoreList = [sort[1] for sort in sortedPhoneList]
    app.logger.info(items)
    if not pageNo:
        if items > 20:
            return render_template("queryResult.html", title = "Your choice Your Device", phoneDetails = phoneList[0:20], cartDetails = cartList, scoreList = scoreList[0:20], prev = 0, next = 2, totItem = items, page = 1, fromItem = 1, toItem = 20, currentURL = currentURL,totalPages = totalPages, pageType=pageType,allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18])
        else :
            return render_template("queryResult.html", title = "Your choice Your Device", phoneDetails = phoneList, cartDetails = cartList, scoreList = scoreList, prev = 0, next = 0, totItem = items, page=0, fromItem = 1, toItem = items, currentURL = currentURL, totalPages = totalPages,pageType=pageType,allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18])
    else:
        pageNo = int(pageNo[0])
        if items > 20*pageNo:
            return render_template("queryResult.html", title = "Your choice Your Device", phoneDetails = phoneList[20*(pageNo-1):(20*(pageNo))], cartDetails = cartList, scoreList = scoreList[20*(pageNo-1):20*(pageNo)], prev = 1, next = pageNo + 1, totItem = items, page = pageNo, fromItem = 20*(pageNo-1) + 1, toItem = 20*pageNo, currentURL = currentURL, totalPages = totalPages, pageType=pageType,allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18])
        else:
            return render_template("queryResult.html", title = "Your choice Your Device", phoneDetails = phoneList[(20*(pageNo-1)):items], cartDetails = cartList, scoreList = scoreList[(20*pageNo-1):items], prev = 1, next = 0, totItem = items, page = pageNo, fromItem = 20*(pageNo-1) + 1, toItem = items, currentURL = currentURL, totalPages = totalPages, pageType=pageType,allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18])
    
    
    return render_template("queryResult.html", title = "Your choice Your Device", phoneDetails = phoneList, cartDetails = cartList, scoreList = scoreList,allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18])


@mod.route('/', methods=['GET'])
def homePage():
    print "Hello"
    cartList = getCartDetails()
    cameraPhoneList = mongo.bestCollection.find_one({'keyword':"Camera"})
    cameraPhoneList = cameraPhoneList['short']
    cameraScoreList = []
    for allPhones in cameraPhoneList:
        finalRating = allPhones['finalRating']
        cameraScoreList.append(finalRating)
    
    batteryPhoneList = mongo.bestCollection.find_one({'keyword':"Battery"})
    batteryPhoneList =  batteryPhoneList['short']
    batteryScoreList = []
    for allPhones in batteryPhoneList:
        finalRating = allPhones['finalRating']
        batteryScoreList.append(finalRating)

    allPhoneList = mongo.bestCollection.find_one({'keyword':"All"})
    allPhoneList =  allPhoneList['short']
    allScoreList = []
    for allPhones in allPhoneList:
        finalRating = allPhones['finalRating']
        allScoreList.append(finalRating)
    return render_template("index-boxed.html", title = "Your choice Your Device",cartDetails = cartList, batteryPhoneList = batteryPhoneList[0:10],batteryScoreList = batteryScoreList[0:10],allPhoneList = allPhoneList[0:10],allScoreList = allScoreList[0:10], cameraPhoneList = cameraPhoneList[0:10], cameraScoreList= cameraScoreList[0:10],allTopBrands = allBrands[0:7],allNonTopBrands = allBrands[11:18])
