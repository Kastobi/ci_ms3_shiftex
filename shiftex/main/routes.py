import time

from flask import render_template

from shiftex.main import main
from shiftex.main import mongo


@main.route("/")
def index():
    today_time = time.strftime("%A, %d %b %Y", time.localtime())
    now_unixtime = int(time.time()) * 1000
    today_duty_list = list(mongo.db.shifts.find(
        {"$and": [
            {"from": {"$lt": now_unixtime}},
            {"to": {"$gt": now_unixtime}}
        ]}))
    return render_template("index.html",
                           today_duty_list=today_duty_list,
                           today_time=today_time)
