from flask import Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mongoengine import MongoEngine

from util import install_secret_key

app = Flask(__name__)
app.config.from_object('config')
app.config["MONGODB_SETTINGS"] = {'DB': "compareDB"}
app.config["SECRET_KEY"] = "JA%*&DNA&D^)A"

db = SQLAlchemy(app)
mongo = MongoEngine(app)

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

# User Views
from app.users.views import mod as usersModule
app.register_blueprint(usersModule)


#Phone Views
from app.phones.views import mod as phonesModule
app.register_blueprint(phonesModule)
