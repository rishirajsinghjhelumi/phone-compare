from flask import Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from util import install_secret_key
import os
from playhouse.flask_utils import FlaskDB

ADMIN_PASSWORD = 'secret'
APP_DIR = os.path.dirname(os.path.realpath(__file__))

# The playhouse.flask_utils.FlaskDB object accepts database URL configuration.
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'blog.db')
DEBUG = False

# The secret key is used internally by Flask to encrypt session data stored
# in cookies. Make this unique for your app.
SECRET_KEY = 'shhh, secret!'
# This is used by micawber, which will attempt to generate rich media
# embedded objects with maxwidth=800.
SITE_WIDTH = 800

app = Flask(__name__)
app.config.from_object(__name__)

app.config["MONGODB_SETTINGS"] = {'DB': "compareDB"}
app.config["SECRET_KEY"] = "JA%*&DNA&D^)A"
db = SQLAlchemy(app)

flask_db = FlaskDB(app)

# The `database` is the actual peewee database, as opposed to flask_db which is
# the wrapper.
database = flask_db.database

mongo = MongoClient('localhost', 27017)['compareDB']

if not app.config['DEBUG']:
    install_secret_key(app)
    
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

#Blog Views
from app.blog.views import mod as blogModule
from app.blog.views import Entry, FTSEntry
database.create_tables([Entry, FTSEntry], safe=True)
app.register_blueprint(blogModule)
