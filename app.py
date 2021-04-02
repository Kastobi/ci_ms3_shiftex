import os
import time

from flask import Flask, render_template
from flask_pymongo import PyMongo

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)


@app.route("/")
def index():
    today_unixtime = int(time.time()) * 1000
    print(today_unixtime)
    today_duty_list = list(mongo.db.emergency_shifts.find(
        {"$and": [
            {"from": {"$lt": today_unixtime}},
            {"to": {"$gt": today_unixtime}}
        ]}))
    return render_template("index.html", today_duty_list=today_duty_list)


if __name__ == "__main__":
    app.run(
        debug=True)
# todo: debug mode !
