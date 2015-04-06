from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from bson.objectid import ObjectId

from bson import json_util
import json

from app import mongo
from app.decorators import mongoJsonify, jsonResponse
from app.util import getArgAsList

mod = Blueprint('phones', __name__, url_prefix='/phone')

def getPhoneInfo(phoneID):
	
	phone = mongo.phones.find_one({
		"_id" : ObjectId(phoneID)
	})
	
	phone["Reviews"] = mongo.reviews.find_one({
		"Brand" : phone["Brand"],
		"Model Name" : phone["Brand"] + " " + phone["Model Name"]
	})["Reviews"]
	
	phone["Sentiments"] = mongo.sentiments.find_one({
		"Brand" : phone["Brand"],
		"Model Name" : phone["Brand"] + " " + phone["Model Name"]
	})["Sentiments"]

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
