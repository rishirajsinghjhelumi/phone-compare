from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify

from app import mongo

mod = Blueprint('phones', __name__, url_prefix='/phone')

@mod.route('/all/', methods=['GET', 'POST'])
def login():
	pass