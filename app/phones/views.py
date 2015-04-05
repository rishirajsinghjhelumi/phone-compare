from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify

from bson import json_util
import json

from app import mongo
from app.decorators import mongoJsonify

mod = Blueprint('phones', __name__, url_prefix='/phone')

@mod.route('/all/', methods=['GET', 'POST'])
@mongoJsonify
def all():
	return mongo.phones.find_one()