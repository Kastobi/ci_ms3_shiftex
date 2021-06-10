"""
File for Config object

The object can handle multiple configurations and store them to call them
via create_app() function.

https://flask.palletsprojects.com/en/2.0.x/config/#configuring-from-python-files
"""

# pylint: disable=unused-import
# env.py is wrongly highlighted

import os

if os.path.exists("env.py"):
    import env


class Config(object):
    """
    Debug for Flask development mode
    Secret_key for sign cookies etc (CSRF prevention)
    Mongo_uri to connect with MongoDB, options included
    https://flask.palletsprojects.com/en/2.0.x/api/#configuration
    """
    DEBUG = os.environ.get("DEBUG")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MONGO_URI = os.environ.get("MONGO_URI")
