"""
shiftex users package
===================

Containing user registration, login, logout, login_manager functionality
and the user dependent main functionality on route user.html

"""

from flask import Blueprint
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

users = Blueprint("users", __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"

from shiftex.users import forms, models, routes
