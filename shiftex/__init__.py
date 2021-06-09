import os

from flask import Flask

from flask_restful import Api
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from shiftex.db import mongo

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")


mongo.init_app(app)

bcrypt = Bcrypt()
bcrypt.init_app(app)

api = Api(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


from shiftex import routes
