from flask import Blueprint
from flask_pymongo import PyMongo

main = Blueprint("main", __name__)
mongo = PyMongo()

from shiftex.main import filters, routes
