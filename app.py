import os
import time
import datetime

from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo

from forms import LoginForm, RegistrationForm

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)


@app.template_filter()
def timestamp_to_readable(timestamp):
    timestamp = timestamp // 1000
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt


@app.route("/")
def index():
    today_time = time.strftime("%A, %d %b %Y", time.localtime())
    now_unixtime = int(time.time()) * 1000
    today_duty_list = list(mongo.db.emergency_shifts.find(
        {"$and": [
            {"from": {"$lt": now_unixtime}},
            {"to": {"$gt": now_unixtime}}
        ]}))
    return render_template("index.html", today_duty_list=today_duty_list, today_time=today_time)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(
        debug=True)
# todo: debug mode !
