import os

if os.path.exists("env.py"):
    import env


class Config:
    IP = os.environ.get("IP")
    PORT = os.environ.get("PORT")

    SECRET_KEY = os.environ.get("SECRET_KEY")

    MONGO_URI = os.environ.get("MONGO_URI")
