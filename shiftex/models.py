import uuid

from flask_login import UserMixin

from shiftex import login_manager
from shiftex.db import mongo


class User(UserMixin):
    """
    https://stackoverflow.com/questions/54992412/flask-login-usermixin-class-with-a-mongodb/55003240
    """
    def __init__(self, user_json):
        self.user_json = user_json
        self.first_name = user_json["first_name"]
        self.last_name = user_json["last_name"]
        self.email = user_json["email"]
        self.drugstoreId = user_json["drugstoreId"]
        self.passwordHash = user_json["passwordHash"]
        self.id = user_json["user_id"]

    @staticmethod
    def register_user(first_name, last_name, email, drugstore_id, password_hash):
        user_id_random = uuid.uuid4().urn
        user_id_taken = mongo.db.users.find_one({"user_id": user_id_random})
        while user_id_taken is not None:
            user_id_random = uuid.uuid4().urn
            user_id_taken = mongo.db.users.find_one({"user_id": user_id_random})

        registration = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "drugstoreId": int(drugstore_id),
            "passwordHash": password_hash,
            "user_id": user_id_random
        }
        mongo.db.users.insert_one(registration)

    @login_manager.user_loader
    def load_user(user_id):
        u = mongo.db.users.find_one({"user_id": user_id})
        if not u:
            return None
        return User(u)
