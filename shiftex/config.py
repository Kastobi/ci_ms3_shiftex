import os

if os.path.exists("env.py"):
    import env


class Config(object):
    DEBUG = os.environ.get("DEBUG")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MONGO_URI = os.environ.get("MONGO_URI")
