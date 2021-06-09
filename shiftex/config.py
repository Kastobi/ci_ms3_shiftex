import os

if os.path.exists("env.py"):
    import env


class Config:
    IP = os.environ.get("IP")
    PORT = int(os.environ.get("PORT"))
    DEBUG = os.environ.get("DEBUG")

    SECRET_KEY = os.environ.get("SECRET_KEY")

    MONGO_URI = os.environ.get("MONGO_URI")
