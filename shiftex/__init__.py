import ssl
import os

from flask import Flask

if os.path.exists("env.py"):
    import env

#from shiftex.config import Config
from shiftex.main import mongo
from shiftex.restlike import api
from shiftex.users import bcrypt, login_manager


#config_class=Config
def create_app():
    app = Flask(__name__)
    #app.config.from_object(config_class)

    api.init_app(app)
    bcrypt.init_app(app)
    mongo.init_app(app, MONGO_URI=os.getenv("MONGO_URI"))
    login_manager.init_app(app)

    from shiftex.main import main
    from shiftex.restlike import restlike
    from shiftex.users import users
    app.register_blueprint(main)
    app.register_blueprint(restlike)
    app.register_blueprint(users)

    return app
