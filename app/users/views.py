from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from flask import jsonify
from werkzeug import check_password_hash, generate_password_hash
from pymongo import MongoClient
from app import db
from app.users.forms import RegisterForm, LoginForm
from app.users.models import User
from app.users.decorators import requires_login
from app import mongo
from app import app
from app.decorators import mongoJsonify, jsonResponse
import logging
from app.util import getArgAsList
from logging.handlers import RotatingFileHandler

mod = Blueprint('users', __name__, url_prefix='/users')

@mod.route('/me/')
@requires_login
def home():
  return jsonify(g.user.getJSON())

@mod.before_request
def before_request():
  g.user = None
  if 'user_id' in session:
    g.user = User.query.get(session['user_id'])

@mod.route('/login/', methods=['GET', 'POST'])
def login():
  """
  Login form
  """
  form = LoginForm(request.form)
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and check_password_hash(user.password, form.password.data):
      session['user_id'] = user.id
      flash('Welcome %s' % user.name)
      return redirect(url_for('users.home'))
    flash('Wrong email or password', 'error-message')
  return render_template("users/login.html", form=form)

@mod.route('/register/', methods=['GET', 'POST'])
def register():
  """
  Registration Form
  """
  form = RegisterForm(request.form)
  if form.validate_on_submit():
    user = User(name=form.name.data, email=form.email.data, \
      password=generate_password_hash(form.password.data))

    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id

    flash('Thanks for registering')

    return redirect(url_for('users.home'))
  return render_template("users/register.html", form=form)

@mod.route('/subscribePrice', methods=['GET', 'POST'])
@jsonResponse
def subscribePrice():
  email = getArgAsList(request, 'email')[0]
  productName = getArgAsList(request, 'productName')[0]
  productId = getArgAsList(request, 'productId')[0]
  priceCutOff = getArgAsList(request, 'priceCutOff')[0]
  mongo = MongoClient('localhost', 27017)['userRequests']
  priceSubscribers = mongo.priceSubscribers
  existEntry = priceSubscribers.find_one({'email':email, 'productName':productName,'priceCutOff':priceCutOff,'status':'A'})
  print existEntry
  if not existEntry:
    priceSubscribers.insert({
    "email" : email,
    "productName" : productName,
    "productId" : productId,
    "priceCutOff" : priceCutOff,
    "status" : 'A'
  })
    return True
  else:
    return False

