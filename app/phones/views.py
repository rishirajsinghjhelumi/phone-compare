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
handler = RotatingFileHandler("/var/www/html/wordpress/phone-compare/app/phones/logs/application.log", maxBytes=10000000, backupCount=5)
#handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

def getPhoneInfo(phoneID):
	app.logger.info(phoneID)
	phone = mongo.phones.find_one({
		"_id" : ObjectId(phoneID)
	})
        app.logger.info(phone)
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
			eComList.extend([eCom])
		phone["Prices"] = eComList
		app.loger.info(phone["Prices"])
        except:
                app.logger.error("Price data not found for phone with ID: ")
                app.logger.error(phoneID)

	try:
		phone["Sentiments"] = mongo.sentiments.find_one({
			"Brand" : phone["Brand"],
			"Model Name" : phone["Brand"] + " " + phone["Model Name"]
		})["Sentiments"]
	except:
		app.logger.error("Sentiment data not found for phone with ID: ")
                app.logger.error(phoneID)

	return phone

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
	# phoneIds = map(ObjectId, phoneIds)
	# phones = mongo.phones.find({
	# 	"_id" : { 
	# 		"$in" : phoneIds
	# 	}
	# })
	return [getPhoneInfo(phone) for phone in phoneIds]
