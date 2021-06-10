"""
shiftex main package - routes module
=====================================

The default route for users not logged in

routes:
    "/" -> index() -> index.html
"""

import time

from flask import render_template

from shiftex.main import main
from shiftex.main import mongo


@main.route("/")
def index():
    """
    standard route for users not logged in
    contains a list of emergency shifts on duty today

    :return: html template
    :kwarg today_duty_list: list of shifts on duty today
    :kwarg today_time: str representation of today date
    """

    today_time = time.strftime("%A, %d %b %Y", time.localtime())
    now_unixtime = int(time.time()) * 1000
    today_duty_list = list(mongo.db.shifts.find(
        {"$and": [
            {"from": {"$lt": now_unixtime}},
            {"to": {"$gt": now_unixtime}}
        ]}))
    print(type(today_time))
    return render_template("index.html",
                           today_duty_list=today_duty_list,
                           today_time=today_time)
