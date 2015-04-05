from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from bson.objectid import ObjectId

from bson import json_util
import json

from app import mongo
from app.decorators import mongoJsonify, jsonResponse
from app.util import getArgAsList

mod = Blueprint('cart', __name__, url_prefix='/cart')

CART = "CART"

@mod.before_request
def before_request():
  if CART not in session:
  	session[CART] = {}

@mod.route('/add/<phoneID>', methods=['GET'])
@jsonResponse
def addToCart(phoneID):
	
	if phoneID not in session[CART]:
		session[CART][phoneID] = True
		return {"status" : "true"}

	return {"status" : "Already in cart!"}

@mod.route('/remove/<phoneID>', methods=['GET'])
@jsonResponse
def removeFromCart(phoneID):
	
	if phoneID not in session[CART]:
		return {"status" : "Not in Cart!"}

	session[CART].pop(phoneID, None)
	return {"status" : "true"}

@mod.route('/get', methods=['GET'])
@jsonResponse
def getCart():
	return session[CART].keys()

@mod.route('/clear', methods=['GET'])
@jsonResponse
def clearCart():
	session[CART] = {}
	return {"status" : "true"}
