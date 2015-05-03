from flask import Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from pymongo import MongoClient

from util import install_secret_key

app = Flask(__name__)
app.config.from_object('config')
app.config["MONGODB_SETTINGS"] = {'DB': "compareDB"}
app.config["SECRET_KEY"] = "JA%*&DNA&D^)A"

db = SQLAlchemy(app)
mongo = MongoClient('localhost', 27017)['compareDB']

if not app.config['DEBUG']:
    install_secret_key(app)

@app.errorhandler(404)
def not_found(error):
    # return render_template('404.html'), 404
    return jsonify(status = "Page Not Found"), 404

@app.errorhandler(403)
def forbidden_page(error):
    return jsonify(status = "Forbidden Page"), 403

@app.errorhandler(500)
def server_error_page(error):
    return jsonify(status = "Server Error"), 500

@app.route('/hello',methods=['GET'])
def hello():
    return "Hello"
# User Views
from app.users.views import mod as usersModule
app.register_blueprint(usersModule)


# Phone Views
from app.phones.views import mod as phonesModule
app.register_blueprint(phonesModule)

# Cart Views
from app.cart.views import mod as cartModule
app.register_blueprint(cartModule)

#WebPages Views
from app.webpages.views import mod as webModule
app.register_blueprint(webModule)
