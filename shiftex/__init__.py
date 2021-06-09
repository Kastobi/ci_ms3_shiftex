from flask import Flask

from shiftex.config import Config
from shiftex.main import mongo
from shiftex.restlike import api
from shiftex.users import bcrypt, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    api.init_app(app)
    bcrypt.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)

    from shiftex.main import main
    from shiftex.restlike import restlike
    from shiftex.users import users
    app.register_blueprint(main)
    app.register_blueprint(restlike)
    app.register_blueprint(users)

    return app