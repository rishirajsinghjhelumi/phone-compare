from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from bson.objectid import ObjectId

from bson import json_util
import json

from app import mongo
from app.decorators import mongoJsonify, jsonResponse

mod = Blueprint('phones', __name__, url_prefix='/phone')

@mod.route('/brand/<brandName>', methods=['GET', 'POST'])
@jsonResponse
def brandModels(brandName):

	phones = mongo.phones.find({"Brand" : brandName}, {"Model Name" : 1})
	return [phone for phone in phones]

@mod.route('/detail/<phoneID>', methods=['GET', 'POST'])
@jsonResponse
def phoneDetail(phoneID):

	phone = mongo.phones.find_one({"_id" : ObjectId(phoneID)})
	return phone
