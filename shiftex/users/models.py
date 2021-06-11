"""
shiftex users package - models module
====================================

Containing User class to use with flask-login

classes:
    User
"""

import uuid

from flask_login import UserMixin

from shiftex.main import mongo
from shiftex.users import login_manager


class User(UserMixin):
    """
    Is loaded with the user document from the MongoDB users collection

    An additional uuid is generated to prepare easy implementation of
    password change functionality (just generate a new one and patch
    user document)
    https://flask-login.readthedocs.io/en/latest/#alternative-tokens

    https://stackoverflow.com/questions/54992412/flask-login-usermixin-class-with-a-mongodb/55003240

    function
        register_user
    """
    def __init__(self, user_json):
        self.user_json = user_json
        self.first_name = user_json["first_name"]
        self.last_name = user_json["last_name"]
        self.email = user_json["email"]
        self.drugstoreId = user_json["drugstoreId"]
        self.drugstoreName = user_json["drugstoreName"]
        self.passwordHash = user_json["passwordHash"]
        self.id = user_json["user_id"]

    @staticmethod
    def register_user(first_name: str, last_name: str, email: str, drugstore_id: int, password_hash: str):
        """
        generates user document from RegisterForm and inserts into users collection
        """
        user_id_random = uuid.uuid4().urn
        user_id_taken = mongo.db.users.find_one({"user_id": user_id_random})
        while user_id_taken is not None:
            user_id_random = uuid.uuid4().urn
            user_id_taken = mongo.db.users.find_one({"user_id": user_id_random})

        drugstore_document = mongo.db.shifts.find_one({"drugstoreId": int(drugstore_id)})
        drugstore_name = drugstore_document["drugstore"]["name"]

        registration = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "drugstoreId": int(drugstore_id),
            "drugstoreName": drugstore_name,
            "passwordHash": password_hash,
            "user_id": user_id_random
        }
        mongo.db.users.insert_one(registration)

    @login_manager.user_loader
    def load_user(user_id):
        """
        Finds user in users collection and loads the user-document
        """
        u = mongo.db.users.find_one({"user_id": user_id})
        if not u:
            return None
        return User(u)
