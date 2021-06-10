"""
shiftex - Organizing shift exchanges in big rotation groups
===========================================================

shiftex is a Full Stack project using Python, JavaScript,
jQuery, MongoDB, HTML and CSS.

It provides a solution for shift exchanges in bigger
anonymous rotation groups.

Read more:
https://github.com/apometricsTK/ci_ms3_shiftex/blob/master/README.md
"""

from flask import Flask

from shiftex.config import Config
from shiftex.main import mongo
from shiftex.restlike import api
from shiftex.users import bcrypt, login_manager


def create_app(config_class=Config):
    """
    Creates the app with Config object, initialises components and returns it
    https://flask.palletsprojects.com/en/2.0.x/config/#configuring-from-python-files

    Config file MUST have "MONGO_URI" and "SECRET_KEY" set,
    otherwise the app won't start.

    :param config_class: Config object
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialise extensions
    api.init_app(app)
    bcrypt.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)

    # import blueprints and register them
    from shiftex.main import main
    from shiftex.restlike import restlike
    from shiftex.users import users
    app.register_blueprint(main)
    app.register_blueprint(restlike)
    app.register_blueprint(users)

    return app
