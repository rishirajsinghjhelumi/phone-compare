from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from bson.objectid import ObjectId

from bson import json_util
import json
import logging
from logging.handlers import RotatingFileHandler
from app import app

from app import mongo
from app.decorators import mongoJsonify, jsonResponse
from app.util import getArgAsList

mod = Blueprint('cart', __name__, url_prefix='/cart')
formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler = RotatingFileHandler("app/phones/logs/application.log", maxBytes=10000000, backupCount=5)
#handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

CART = "CART"

@mod.before_request
def before_request():
  if CART not in session:
  	session[CART] = {}

@mod.route('/add/<phoneID>', methods=['GET'])
@jsonResponse
def addToCart(phoneID):

	if len(session[CART]) == 4:
		return {"status" : 512, "phoneId" : session[CART]}


	if phoneID not in session[CART]:
		session[CART][phoneID] = True
		# statusCode : 256   already present
		# status code  :512  4 phone already present
		app.logger.info(len(session[CART]))
		return {"status" : 200, "count": len(session[CART]), "phoneId" : session[CART].keys()}

	return {"status" : 256}

@mod.route('/remove/<phoneID>', methods=['GET'])
@jsonResponse
def removeFromCart(phoneID):
	
	if phoneID not in session[CART]:
		return {"status" : "Not in Cart!", "phoneId" : session[CART].keys()}

	session[CART].pop(phoneID, None)
	return {"status" : "true"}

@mod.route('/get', methods=['GET'])
@jsonResponse
def getCart():
	return session[CART].keys()

def getCartDetails():
	cartDetails = {}
	cartDetails =  session[CART].keys()
	app.logger.info(cartDetails)
	return cartDetails
	# cartContent = [keys for keys in cartDetails]
	
	# app.logger.info(cartContent)
	# return cartContent

@mod.route('/clear', methods=['GET'])
@jsonResponse
def clearCart():
	session[CART] = {}
	return {"status" : "true"}
