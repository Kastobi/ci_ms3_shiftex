"""
shiftex main package
===================

Containing basic route, utility jinja-template_filter
and the basic database object.

"""

from flask import Blueprint
from flask_pymongo import PyMongo

main = Blueprint("main", __name__)
mongo = PyMongo()

from shiftex.main import filters, routes
